from django import forms
from .models import *

class FieldForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['title','company','location','job_type','category','description','salaryBottom','salaryTop','requirement']
        widgets = {'job_type':forms.RadioSelect}