from django.urls import path
from . import views


urlpatterns = [
path('users/', views.GetUsers.as_view()),
path('register/', views.CreateUser.as_view()),
path('users/<int:id>', views.UpdateUser.as_view())
]