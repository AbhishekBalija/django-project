from django.http import HttpResponse
from django.shortcuts import render
from delivery.models import Customer

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
        fullname = request.POST.get('fullname', '').strip(),
        email = request.POST.get('email', '').strip() ,
        password = request.POST.get('password', '').strip(),
        phone = request.POST.get('phone', '').strip(),
        address = request.POST.get('address', '').strip()

        info = {
            'fullname': fullname,
            'password': password,
            'email': email,
            'phone': phone,
            'address': address,
        }
        # Save to db
        c = Customer(fullname = fullname,password = password, email = email, phone = phone, address = address)
        c.save()

        return render(request, 'delivery/SignUpInfo.html',info) 
    else:
        return HttpResponse(f"Invalid signup form")


