from django.urls import path

from .views import (
	UserDetailApiView, 
	UserCreationApiView,
	UserUpdateApiView,
	UserActivateApiView,
)


app_name = "api"
urlpatterns = [
	
	path("user-create", UserCreationApiView.as_view()),

	path("detail-user/<str:username>/<str:password>/",
		UserDetailApiView.as_view()),
	path("user-update/<str:username>/<str:password>/", 
		UserUpdateApiView.as_view()),
	path("user-activate/<str:username>/<str:password>/",
		UserActivateApiView.as_view()),

]