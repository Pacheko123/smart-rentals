from django.db import models 

# Create your models here.

class Apartment(models.Model):
	apart_name = models.CharField(max_length = 24)
	# apartment_number = models.CharField(max_length = 24, unique = True)

class Tuser(models.Model):
	"""docstring for Student"""
	username = models.CharField(max_length = 24)
	password = models.CharField(max_length = 24)
	mail = models.CharField(max_length = 34,default = 'test@gmail.com')
	apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank = True , null = True)

class transactions(models.Model):
	name = models.CharField(max_length = 34)
	
		
