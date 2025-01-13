from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signin/', views.signin),
    path('signup/', views.signup),
    path('signin/signup/', views.signup),
    path('signup/signin/', views.signin),
    path('handle_signin/', views.handleSignin, name='handleSignin'),
    path('handleSignup/', views.handleSignup, name='handleSignup'),
]