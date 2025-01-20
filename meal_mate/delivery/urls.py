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
    path('handle_signin/restaurant_page/', views.restaurant_page, name='restaurant_page'),
    path('handle_signin/view_restaurants/', views.view_restaurants, name='view_restaurants'),
    path('handle_signin/add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('handle_signin/view_restaurants/restaurant_menu/<int:restaurant_id>/', views.restaurant_menu, name='restaurant_menu'),
]
