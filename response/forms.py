from django import forms
from .models import *

class CreateJobForm(forms.ModelForm):
    company=forms.CharField(widget=forms.TextInput(
        attrs={
            'class':'font-weight-bold form-control',
            'style':'margin:20px;',
        }
        ))
    class Meta:
        model = Job
        fields = ['title','company','location','job_type','category','description','salaryBottom','salaryTop','requirement']
        widgets = {'job_type':forms.RadioSelect}