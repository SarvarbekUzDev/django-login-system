from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from random import randint

from users.models import CustomUser
# from .serializers import UserSerializer

# Create your views here.
class UserDetailApiView(APIView):
	# get method
	def get(self, request, username, password):
		data = {}
		data["Ok"] = True
		data["status"] = 200
		data["message"] = None

		user = CustomUser.objects.filter(username=username, password2=password,
											is_active=True)
		if user.exists():
			data["message"] = "Ok."
			data["data"] = user.values()
		else:
			data["status"] = 400
			data["message"] = "This user does not exist or has not been activated."
		
		return Response(data, status=data["status"])

# User Create.
class UserCreationApiView(APIView):
	# post method
	def post(self, request):
		data = {}
		data["Ok"] = True
		data["status"] = 200
		data["message"] = None

		try:
			username = request.data.get("username")
			email = request.data.get("email")
			password = request.data.get("password")
			rand_number = randint(10000, 99999)
			if username and email and password and len(password) >=  8:
				new_user = CustomUser.objects.create(
					username=username,
					email=email,
					password2=password,
					rand_number=rand_number,
					is_active=False
				)
				new_user.set_password(password)
				new_user.save()

				data["message"] = "Ok."
				data["data"] = {"username":username, "email":email, "password":password}
			else:
				data["Ok"] = False
				data["status"] = 400
				data["message"] = "Enter the details completely. (username, email, password)"
		except Exception as e:
			print(e)
			data["Ok"] = False
			data["status"] = 400
			data["message"] = "Some error. Or the user already exists."
		
		return Response(data, status=data["status"])


# User Update.
class UserUpdateApiView(APIView):
	# post method
	def post(self, request, username, password):
		data = {}
		data["Ok"] = True
		data["status"] = 200
		data["message"] = None

		try:
			username_edit = request.data.get("username")
			password_edit = request.data.get("password")
			if username and password and username_edit and password_edit:
				user = CustomUser.objects.get(username=username, password2=password)
				user.username = username_edit
				user.password2 = password_edit
				user.save()

				data["message"] = "Ok."
			else:
				data["Ok"] = False
				data["status"] = 400
				data["message"] = "`username` and `password` are not included."
		except Exception as e:
			data["Ok"] = False
			data["status"] = 400
			data["message"] = "Some error. Or the user information is wrong."
		

		return Response(data, status=data["status"])

# Activate User Api View
class UserActivateApiView(APIView):
	# get method
	def post(self, request, username, password):
		data = {}
		data["Ok"] = True
		data["status"] = 200
		data["message"] = None

		rand_number = request.data.get("rand_number")
		try:
			if rand_number:
				user = CustomUser.objects.get(username=username, password2=password,
											rand_number=rand_number)
				user.is_active = True
				user.save()

				data["message"] = "Ok. User active."
			else:
				data["Ok"] = False
				data["status"] = 400
				data["message"] = "`rand_number` is not included."
		except Exception as e:
			data["Ok"] = False
			data["status"] = 400
			data["message"] = "Some error or user does not exist."


		return Response(data, status=data["status"])