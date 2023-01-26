from django.urls import path

from .views import SignUpView, LoginView, LogoutView, UserActivateView

app_name = "users"
urlpatterns = [
	path("signup/", SignUpView.as_view(), name="signup"),
	path("user_activate/<str:username>/", UserActivateView, name="useractivate"),
	path("login/", LoginView.as_view(), name="login"),
	path("logout/", LogoutView, name="logout"),
]