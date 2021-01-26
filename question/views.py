from django.shortcuts import render, redirect
from .models import *
from django.core import mail
from django.core.mail import send_mail,EmailMessage
from django.views.generic import CreateView, UpdateView, DetailView,ListView, View
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
	msg_html = render_to_string(template_name, context)
	msg = EmailMessage(subject=subject, body=msg_html, from_email=sender, bcc=[to_list])
	msg.content_subtype = "html"  # Main content is now text/html
	return msg.send()

def email_confirmation(request, email, response, form ):
	emails = email
	context = {
		'code': response.code,
		'form': form,
		'response':response
	}
	send_html_email(emails, 'Email Confirmation', 'question/email.html', context, "info@example.org")

class AdminView(LoginRequiredMixin,ListView):
	model 				= Form
	template_name		='admin/admin.html'
	queryset 	  		= Form.objects.all()

class ResponseView(LoginRequiredMixin,ListView):
	model 				= Response
	template_name		='admin/response.html'

	def get_context_data(self, **kwargs):
		context = super(ResponseView, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']
		form = Form.objects.get(slug=slug)
		response = form.response.all()
		context['response'] = response
		context['form'] = form
		return context

def completion(request, *args, **kwargs):
	slug=kwargs['slug']
	code = kwargs['code']
	res_slug=kwargs['res_slug']

	context={
		'form': Form.objects.get(slug=slug),
		'response':Response.objects.get(slug=res_slug),
		'email':Response.objects.get(slug=res_slug).email,
		'code': code,
	}		
	return render(request,'question/completion.html',context)

class FormAnswer(LoginRequiredMixin,ListView):
	model = Response
	template_name='admin/form_answer.html'

	def get_context_data(self, **kwargs):
		context = super(FormAnswer, self).get_context_data(**kwargs)
		slug = self.kwargs['slug']
		res_slug = self.kwargs['code']

		form = Form.objects.get(slug=slug)
		response = Response.objects.get(slug=res_slug)

		context['response'] = response
		context['form'] = form
		return context

class QuestionView(DetailView):
	model = Form
	template_name = 'question/question.html'	

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		slug=self.kwargs["slug"]		
		form = Form.objects.get(slug=slug)
		context['form'] = form
		context['field'] = form.field.all()
		try:
			multiple = field.multiple.all()
		except:
			multiple = None
		context['multiple'] = multiple
		return context

	def post(self, request, *args, **kwargs):
		allowed_chars = ''.join((string.ascii_letters, string.digits))
		unique_url = ''.join(random.choice(allowed_chars) for _ in range(32))

		slug  	= self.request.POST['slug']
		email 	= self.request.POST['email']
		form 	= Form.objects.get(slug=slug)

		response = Response.objects.create(form_response=form.form_name,email=email,slug = unique_url)
		response.save()
		form.response.add(response)
		form.save()

		for a in form.field.all():
			answer = Answer.objects.create(answer=self.request.POST[a.field_name], question=a.field_name, variable=a.variable, field_type=a.field_type)
			answer.save()
			response.answer.add(answer)
			response.save()

		email_confirmation(self.request, email, response, form)
		code = response.slug
		url = '../{}/{}'.format(slug, code)
		print(url) 
		return redirect(url)





