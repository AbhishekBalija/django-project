from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication paths
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.handleSignin, name='handleSignin'),
    path('customer-home/', views.customer_home, name='customer_home'), 
    path('signup/submit/', views.handleSignup, name='handle_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Restaurant-related paths
    path('restaurants/', views.view_restaurants, name='show_restaurant_page'),
    path('restaurants/add/', views.add_restaurant, name='add_restaurant'),
    path('restaurants/<int:restaurant_id>/', views.restaurant_page, name='restaurant_page'),
    path('restaurants/<int:restaurant_id>/menu/', views.restaurant_menu, name='restaurant_menu'),
    path('restaurants/<int:restaurant_id>/update/', views.edit_restaurant, name='update_restaurant'),
    path('restaurants/<int:restaurant_id>/delete/', views.delete_restaurant, name='delete_restaurant'),
    path('logout/', views.logout_view, name='logout'),

    # Menu-related paths
    path('restaurants/<int:restaurant_id>/menu/<int:item_id>/edit/', views.edit_menu_item, name='edit_menu_item'),
    path('restaurants/<int:restaurant_id>/menu/<int:item_id>/delete/', views.delete_menu_item, name='delete_menu_item'),

    # Customer-related paths
    path('restaurants/<int:restaurant_id>/customermenu/', views.customer_menu, name='customer_menu'),

    # Cart-related paths
    path('cart/', views.show_cart_page, name='show_cart_page'),
    path('cart/add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),

]