from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from delivery.models import Customer, MenuItem, Restaurant

# Create your views here.

def index(request):
    return render(request, 'delivery/index.html')

def signin(request):
    return render(request, 'delivery/SignIn.html')

def signup(request):
    return render(request, 'delivery/SignUp.html')

def handleSignin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')  
        password = request.POST.get('password')

        try:
            cust = Customer.objects.get(fullname=fullname, password=password)
            return render(request, 'delivery/Home.html')
        except:
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

        try:
            # Check if customer already exists
            Customer.objects.get(fullname = fullname)
            return render(request, 'delivery/SignUp.html', {'error_message': 'Username already exists'})
        except:
            # Save to db
            c = Customer(fullname = fullname,password = password, email = email, phone = phone, address = address)
            c.save()

        return render(request, 'delivery/SignIn.html') 
    else:
        return HttpResponse(f"Invalid signin form")

def restaurant_page(request):
    return render(request,'delivery/AddRestaurant.html')

def view_restaurants(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/ViewRestaurant.html',{"restaurants":restaurants})


def add_restaurant(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        restaurant_cuisines = request.POST.get('restaurant_cuisines')
        restaurant_address = request.POST.get('restaurant_address')
        restaurant_rating = request.POST.get('restaurant_rating')
        restaurant_photo = request.POST.get('restaurant_photo')

        try: 
            # Check if restaurant already exists
            Restaurant.objects.get(restaurant_name = restaurant_name)
            return render(request, 'delivery/AddRestaurant.html', {'error_message': 'Restaurant already exists'})
        except:
            rest = Restaurant(restaurant_name=restaurant_name,restaurant_cuisines=restaurant_cuisines,restaurant_address=restaurant_address,restaurant_rating=restaurant_rating,restaurant_photo=restaurant_photo)
            rest.save()

        restaurants = Restaurant.objects.all()

        return render(request, 'delivery/ViewRestaurant.html',{"restaurants":restaurants}) 
    else:
        return HttpResponse(f"Invalid Request")

def restaurant_menu(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        photo = request.POST.get('photo')

        MenuItem.objects.create(
            name=name,
            description=description,
            price=price,
            photo=photo,
            restaurant=restaurant,
        )

        return redirect('restaurant_menu', restaurant.id)

    # Fetch all menu items for this restaurant
    menu_items = restaurant.menu_items.all()

    return render(request, 'delivery/AddItem.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
    })
