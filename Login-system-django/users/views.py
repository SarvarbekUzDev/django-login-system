from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 
from django.http.request import QueryDict, MultiValueDict
from django.http import Http404
from django.contrib import messages  
from django.conf import settings
from random import randint

from .models import CustomUser
from .forms import CustomUserForm
# from .signals import send_password_mail


# Sign Up View
class SignUpView(View):
	# Dispatcher method
	def dispatch(self, request):
		if request.method == "GET":
			return self.get(request)
		if request.method == "POST":
			return self.post(request)

	# Get method
	def get(self, request):
		# send_password_mail()
		form = CustomUserForm()
		return render(request, "users/signup.html", {"form":form})

	# Post method
	def post(self, request):
		form = CustomUserForm(data=request.POST)
		if form.is_valid():
			try:
				rand_number = randint(10000, 99999)
				# send email
				send_mail(
					"Code",
					f"{rand_number}",
					settings.EMAIL_HOST_USER,
					[f"{request.POST.get('email')}"],
					fail_silently=False,
				)

				# User Create
				user = form.save(commit=False)
				user.password2 = request.POST.get("password")
				user.rand_number = rand_number
				user.is_active = False
				user.save()
				
				return redirect("users:useractivate", request.POST.get("username"))
			except ZeroDivisionError as e:
				messages.error(request, "Error!")
				return render(request, "users/signup.html", {"form":form})

		messages.error(request, f"{form.errors.as_text()}")
		return render(request, "users/signup.html", {"form":form})


# Login View
class LoginView(View):
	# Dispatcher method
	def dispatch(self, request):
		if request.method == "GET":
			return self.get(request)
		if request.method == "POST":
			return self.post(request)

	# Get method
	def get(self, request):
		return render(request, 'users/login.html', {})

	# Post method
	def post(self, request):
		login_form = AuthenticationForm()
		error_text = "Please enter a correct username and password. Note that both fields may be case-sensitive."
		user = CustomUser.objects.filter(email=request.POST.get("email"),
			password2=request.POST.get("password"))
		if user.exists():
			if user.get().is_active:
				data = {'csrfmiddlewaretoken': [request.POST.get("csrfmiddlewaretoken")], 'username': [user.get().username], 'password': [request.POST.get("password")]}
				query_dict = QueryDict("", mutable=True)
				query_dict.update(MultiValueDict(data))
				login_form = AuthenticationForm(data=query_dict)

				if login_form.is_valid():
					user=login_form.get_user()
					login(request, user)

					messages.success(request, f'Welcom {request.user}')
					return redirect('home')
				else:
					messages.error(request, f"{login_form.errors.as_text()}")
					return render(request, 'users/login.html', {'form':login_form})
			else:
				return redirect("users:useractivate", user.get().username)
		else:
			messages.error(request, error_text)
			return render(request, 'users/login.html', {"form":login_form})

# Logout
def LogoutView(request):
	logout(request)
	messages.info(request, "Logout!")

	return redirect("home")


# User active
def UserActivateView(request, username):
	user = CustomUser.objects.get(username=username)
	if request.method == "GET":
		if user.is_active:
			raise Http404

		return render(request, "users/user_activate.html", {"user_activate":user})

	if request.method == "POST":
		password = request.POST.get("password")
		if str(user.rand_number) == str(password):
			edit = user
			edit.is_active = True
			edit.save()

			return redirect("users:login")
		else:
			return render(request, "users/user_activate.html", {"user_activate":user, "error_message":True})
