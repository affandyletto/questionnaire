from django.shortcuts import render,redirect
from question.models import *
from django.core.mail import send_mail, EmailMessage
from django.views.generic import CreateView, UpdateView, DetailView,ListView, View
from django.template.loader import render_to_string
from django.conf import settings
import string
import random
from django.urls import reverse
from django.http import HttpResponseRedirect

class ResultView(View):
	model = Response
	template_name = 'question/result.html'

	def get(self,request,*args,**kwargs):
		slug 	= kwargs["slug"]
		code 	= kwargs['code']
		response = Response.objects.get(slug=code)
		form 	= Form.objects.get(slug=slug)
		context={
			'form':form,
			'email':response.email,
			'code': code,
		}
		return render(self.request,'question/result.html',context)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

	def post(self, request, *args, **kwargs):
		slug_res = kwargs["code"]
		slug = kwargs["slug"]
		form = Form.objects.get(slug=slug)
		response = Response.objects.get(slug=slug_res)
		code=response.code
		if code == request.POST['code']:
			context={
				'form': form,
				'response':response,
				'email':response.email,
				'code': response.code,
			}		
			print("password benar")		
			return render(request,'question/completion.html',context)
		else:
			return HttpResponseRedirect('../../wrong')
