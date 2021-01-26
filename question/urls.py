from django.urls import path
from .views import *
from response.views import *
from django.views.generic import TemplateView
import random
import string

allowed_chars = ''.join((string.ascii_letters, string.digits))
unique_id = ''.join(random.choice(allowed_chars) for _ in range(32))
app_name = 'question'

urlpatterns = [
	path('wrong/', TemplateView.as_view(template_name="question/wrong.html"),name="wrong"),
    path('<slug:slug>/',QuestionView.as_view(),name="question"),
    path('<slug:slug>/response/<slug:code>/',FormAnswer.as_view(),name="form_answer"),
    path('<slug:slug>/<slug:code>/',ResultView.as_view(),name="result"),
    path('<slug:slug>/<slug:code>/<slug:res_slug>/document',completion,name="completion"),
]