from django.db import models
from django.utils.text import slugify
import string
import random

class Answer(models.Model):
	variable 	= models.CharField(max_length=10,default=None,blank=True, null = True)
	field_type 	= models.CharField(max_length=30,default=None,blank=True)
	question=models.CharField(max_length=10,default=None,blank=True)
	answer=models.CharField(max_length=10,default=None,blank=True)

	def __str__(self):
		return self.question

def rand_slug():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

def rand_code():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(4))

class Response(models.Model):  
	form_response 	= models.CharField(max_length=300)
	answer 			= models.ManyToManyField(Answer,default=None,blank=True,related_name="form")
	slug 			= models.CharField(max_length=300)
	email 			= models.CharField(max_length=300,default=None,blank=True)
	code 			= models.SlugField(max_length=255, unique=True,default=None,blank=True)

	def save(self, *args, **kwargs):
		if not self.code:
			self.code = slugify(rand_code())
		super(Response, self).save(*args, **kwargs)

	def delete(self,*args, **kwargs):
		print("masuk sini couutt")
		self.answer.all().delete()	    
		super(Response, self).delete(*args, **kwargs)

	def __str__(self):
		return self.form_response