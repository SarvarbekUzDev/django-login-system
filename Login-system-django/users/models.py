from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
	email = models.EmailField(unique=True)
	password2 = models.CharField(max_length=150, blank=True)
	rand_number = models.CharField(max_length=100, blank=True)
	is_active = models.BooleanField(default=True)


	def __str__(self):
		return self.username