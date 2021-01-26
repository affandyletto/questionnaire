from django.db import models
from response.models import *
from django.utils.text import slugify
import string
import random

class Multiple(models.Model):
	text=models.CharField(max_length=10,default=None,blank=True)
	
	def __str__(self):
		return self.text

class Field(models.Model):
	field_name 	= models.CharField(max_length=300)
	variable_choices = (
		('p','p'),
		('h1','h1'),
		('h2','h2'),
		('h3','h3'),
		('a','a'),
	)
	type_choices =(
		('Text Area','Text Area'),
		('Text Input','Text Input'),
		('Drop Down','Drop Down'),
		('Check Box','Check Box'),
	)
	variable 	= models.CharField(max_length=10,default=None,blank=True, null = True, choices=variable_choices)
	field_type 	= models.CharField(max_length=30,default=None,blank=True, choices=type_choices)
	multiple 	= models.ManyToManyField(Multiple,default=None,blank=True, null = True, related_name="field")
	required 	= models.BooleanField(default=False)

	def __str__(self):
		return self.field_name

def rand_slug():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

class Form(models.Model):
	form_name 		= models.CharField(max_length=300)
	document_title 	= models.CharField(max_length=300,default=None,blank=True)
	file_name 		= models.CharField(max_length=300,default=None,blank=True)
	text_container1 = models.CharField(max_length=300,default=None,blank=True)
	text_container2 = models.CharField(max_length=300,default=None,blank=True)
	text_completion = models.TextField(default=None,blank=True)
	field 			= models.ManyToManyField(Field,related_name="form")
	response 		= models.ManyToManyField(Response,default=None,blank=True,related_name="form")
	slug 			= models.SlugField(max_length=255, unique=True,default=None,blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(rand_slug() + "-" + self.form_name)

		super(Form, self).save(*args, **kwargs)

	def __str__(self):
		return self.form_name