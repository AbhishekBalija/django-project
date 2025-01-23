from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from delivery.models import Customer, MenuItem, Restaurant, CartList
from decimal import Decimal  # Import Decimal for type consistency

# Create your views here.

def index(request):
    return render(request, 'delivery/index.html')

def signin(request):
    return render(request, 'delivery/SignIn.html')

def signup(request):
    return render(request, 'delivery/SignUp.html')

def dashboard(request):
    return render(request, 'delivery/Home.html')

def handleSignin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')  
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(fullname=fullname, password=password)
            if fullname == 'admin':
                return render(request, 'delivery/Home.html')
            else:
                # Store fullname and customer_id in session
                request.session['fullname'] = customer.fullname
                request.session['customer_id'] = customer.id  # Store customer_id

                restaurants = Restaurant.objects.all()
                context = {
                    'restaurants': restaurants,
                    'fullname': customer.fullname
                }
                return render(request, 'delivery/CustomerHome.html', context)
        except Customer.DoesNotExist:
            error_message = "Invalid fullname or password"
            return render(request, 'delivery/SignIn.html', {'error_message': error_message})
    else:
        return HttpResponse("Invalid request")     

def handleSignup(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if Customer.objects.filter(fullname=fullname).exists():
            return render(request, 'delivery/SignUp.html', {'error_message': 'Username already exists'})
        
        Customer.objects.create(fullname=fullname, password=password, email=email, phone=phone, address=address)
        messages.success(request, 'Account created successfully!')
        return redirect('signin')
    else:
        return HttpResponse("Invalid signup form")

def logout_view(request):
    logout(request)
    if 'fullname' in request.session:
        del request.session['fullname']
    return redirect('index')

def restaurant_page(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'delivery/RestaurantPage.html', {'restaurant': restaurant})

def view_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/ViewRestaurant.html', {"restaurants": restaurants})

def add_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_cuisines = request.POST.get('restaurant_cuisines')
        restaurant_address = request.POST.get('restaurant_address')
        restaurant_rating = request.POST.get('restaurant_rating')
        restaurant_photo = request.POST.get('restaurant_photo')

        if Restaurant.objects.filter(restaurant_name=restaurant_name).exists():
            return render(request, 'delivery/AddRestaurant.html', {'error_message': 'Restaurant already exists'})

        Restaurant.objects.create(
            restaurant_name=restaurant_name,
            restaurant_cuisines=restaurant_cuisines,
            restaurant_address=restaurant_address,
            restaurant_rating=restaurant_rating,
            restaurant_photo=restaurant_photo
        )
        messages.success(request, 'Restaurant added successfully!')
        return redirect('show_restaurant_page')
    else:
        # Add this to handle GET requests
        return render(request, 'delivery/AddRestaurant.html')

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        photo = request.POST.get('photo')
        is_veg=request.POST.get('is_veg') == '1'

        MenuItem.objects.create(
            name=name,
            description=description,
            price=price,
            photo=photo,
            restaurant=restaurant,
            is_veg=is_veg,
        )
        messages.success(request, 'Menu Item added successfully!')
        return redirect('restaurant_menu', restaurant_id=restaurant.id)

    menu_items = restaurant.menu_items.all()
    return render(request, 'delivery/AddItem.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })

def edit_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        restaurant.restaurant_name = request.POST.get('restaurant_name')
        restaurant.restaurant_cuisines = request.POST.get('restaurant_cuisines')
        restaurant.restaurant_address = request.POST.get('restaurant_address')
        restaurant.restaurant_rating = request.POST.get('restaurant_rating')
        restaurant.restaurant_photo = request.POST.get('restaurant_photo')
        
        restaurant.save()
        messages.success(request, 'Restaurant updated successfully!')
        return redirect('show_restaurant_page')
        
    return render(request, 'delivery/EditRestaurant.html', {'restaurant': restaurant})

def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant.delete()
    messages.success(request, 'Restaurant deleted successfully!')
    return redirect('show_restaurant_page')


def edit_menu_item(request, restaurant_id, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant_id=restaurant_id)
    
    if request.method == 'POST':
        menu_item.name = request.POST.get('name')
        menu_item.description = request.POST.get('description')
        menu_item.price = request.POST.get('price')
        menu_item.photo = request.POST.get('photo')
        menu_item.is_veg = request.POST.get('is_veg') == '1'
        
        menu_item.save()
        messages.success(request, 'Menu item updated successfully!')
        return redirect('restaurant_menu', restaurant_id=restaurant_id)
        
    return render(request, 'delivery/EditMenuItem.html', {'menu_item': menu_item})

def delete_menu_item(request, restaurant_id, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id, restaurant_id=restaurant_id)
    menu_item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('restaurant_menu', restaurant_id=restaurant_id)


# Customer Menu
def customer_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    return render(request, 'delivery/CustomerMenu.html', {'restaurant': restaurant, 'menu_items': menu_items})

# Show Cart Page

def show_cart_page(request):
    customer_id = request.session.get('customer_id')  # Get customer ID from session

    if not customer_id:
        return redirect('signin')  # Redirect to login if customer ID is missing

    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = CartList.objects.filter(customer=customer)

    # Calculate subtotal (sum of all items)
    subtotal = sum(item.total_price() for item in cart_items)

    # Define discount and shipping fees as Decimal
    discount = Decimal("50.00")  # Convert float to Decimal
    shipping_fees = Decimal("40.00")  # Convert float to Decimal

    # Calculate total
    total = subtotal - discount + shipping_fees

    return render(request, "delivery/Cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "shipping_fees": shipping_fees,
        "total": total,
    })

# Add to Cart

def add_to_cart(request, item_id):
    customer_id = request.session.get('customer_id')  # Get customer_id from session

    if not customer_id:
        return redirect('signin')  # Redirect to login if customer_id is missing

    customer = get_object_or_404(Customer, id=customer_id)
    menu_item = get_object_or_404(MenuItem, id=item_id)

    cart_item, created = CartList.objects.get_or_create(customer=customer, menu_item=menu_item)

    if not created:
        cart_item.quantity += 1  # Increase quantity if item already exists
        cart_item.save()

    return redirect("show_cart_page")  # No need to pass customer_id

# Remove from Cart

def remove_from_cart(request, item_id):
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('signin')  # Redirect to login if customer_id is missing

    customer = get_object_or_404(Customer, id=customer_id)
    cart_item = get_object_or_404(CartList, customer=customer, menu_item_id=item_id)
    cart_item.delete()

    return redirect("show_cart_page")  # No need to pass customer_id