from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import logout
from delivery.models import Customer, MenuItem, Restaurant, CartList
from decimal import Decimal  # Import Decimal for type consistency
from django.db.models import Q
from django.conf import settings
import razorpay

# Create your views here.

def index(request):
    customer_id = request.session.get('customer_id')
    cart_item_count = get_cart_item_count(customer_id)
    return render(request, 'delivery/index.html', {'cart_item_count': cart_item_count})

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
            request.session['fullname'] = customer.fullname
            request.session['customer_id'] = customer.id
            
            # Redirect based on user role
            if customer.fullname.lower() == 'admin':
                return redirect('dashboard')  # Redirect to admin dashboard
            else:
                return redirect('customer_home')  # Redirect regular customers
            
        except Customer.DoesNotExist:
            error_message = "Invalid fullname or password"
            return render(request, 'delivery/SignIn.html', {'error_message': error_message})
    else:
        return render(request, 'delivery/SignIn.html')

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
    
    # Get the cart item count for the logged-in customer
    customer_id = request.session.get('customer_id')
    cart_item_count = CartList.objects.filter(customer_id=customer_id).count() if customer_id else 0

    return render(request, 'delivery/CustomerMenu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'cart_item_count': cart_item_count  # Pass the cart item count to the template
    })

# Show Cart Page

def show_cart_page(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return redirect('signin')

    customer = get_object_or_404(Customer, id=customer_id)
    cart_items = CartList.objects.filter(customer=customer)

    subtotal = sum(item.total_price() for item in cart_items)
    discount = Decimal("50.00")
    shipping_fees = Decimal("40.00")
    total = subtotal - discount + shipping_fees

    cart_item_count = get_cart_item_count(customer_id)

    return render(request, "delivery/Cart.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "shipping_fees": shipping_fees,
        "total": total,
        "cart_item_count": cart_item_count
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

# Update cart quantity
def update_cart_quantity(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        if not customer_id:
            messages.error(request, 'You must be logged in to update your cart.')
            return redirect('signin')

        item_id = request.POST.get('item_id')
        action = request.POST.get('action')  # 'increase' or 'decrease'

        try:
            customer = Customer.objects.get(id=customer_id)
            cart_item = CartList.objects.get(customer=customer, menu_item_id=item_id)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()
            messages.success(request, 'Cart updated successfully!')

        except (Customer.DoesNotExist, CartList.DoesNotExist):
            messages.error(request, 'Item not found in cart.')

    return redirect('show_cart_page')

def get_cart_item_count(customer_id):
    if customer_id:
        return CartList.objects.filter(customer_id=customer_id).count()
    return 0

# Remove from Cart
def remove_from_cart(request):
    if request.method == 'POST':
        customer_id = request.session.get('customer_id')
        if not customer_id:
            messages.error(request, 'You must be logged in to update your cart.')
            return redirect('signin')

        item_id = request.POST.get('item_id')

        try:
            customer = Customer.objects.get(id=customer_id)
            cart_item = CartList.objects.get(customer=customer, menu_item_id=item_id)
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')

        except (Customer.DoesNotExist, CartList.DoesNotExist):
            messages.error(request, 'Item not found in cart.')

    return redirect('show_cart_page')


# Search Restaurants

def customer_home(request):
    # Check if the user is logged in
    if 'customer_id' not in request.session:
        return redirect('handleSignin')  # Redirect to login if not authenticated

    # Get the search query from the request
    search_query = request.GET.get('search', '')

    # Filter restaurants by name or address
    if search_query:
        restaurants = Restaurant.objects.filter(
            Q(restaurant_name__icontains=search_query) | 
            Q(restaurant_address__icontains=search_query)
        )
    else:
        restaurants = Restaurant.objects.all()

    # Get the cart item count for the logged-in customer
    customer_id = request.session.get('customer_id')
    cart_item_count = CartList.objects.filter(customer_id=customer_id).count() if customer_id else 0

    context = {
        'restaurants': restaurants,
        'cart_item_count': cart_item_count,
        'search_query': search_query  # Pass the search query to the template
    }
    return render(request, 'delivery/CustomerHome.html', context)


def checkout(request, fullname):
    # Fetch customer using fullname
    customer = get_object_or_404(Customer, fullname=fullname)
    cart_items = CartList.objects.filter(customer=customer)

    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items)

    if total_price == 0:
        return render(request, 'delivery/checkout.html', {
            'error': 'Your cart is empty!',
        })

    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create Razorpay order
    order_data = {
        'amount': int(total_price * 100),  # Amount in paisa
        'currency': 'INR',
        'payment_capture': '1',  # Automatically capture payment
    }
    order = client.order.create(data=order_data)

    # Pass the order details to the frontend
    return render(request, 'delivery/checkout.html', {
        'fullname': fullname,
        'cart_items': cart_items,
        'total_price': total_price,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],  # Razorpay order ID
        'amount': total_price,
    })

def orders(request, fullname):
    customer = get_object_or_404(Customer, fullname=fullname)
    cart_items = CartList.objects.filter(customer=customer)

    # Calculate total price
    total_price = sum(item.total_price() for item in cart_items)

    # Clear the cart after fetching its details
    cart_items.delete()

    return render(request, 'delivery/orders.html', {
        'fullname': fullname,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })