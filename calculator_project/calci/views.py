from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'calci/index.html')

def calculate(request):
    if request.method == 'POST':
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        operation = request.POST.get('operation')
        
        try:
            if operation == 'ADD':
                result = num1 + num2
            elif operation == 'SUB':
                result = num1 - num2
            elif operation == 'MUL':
                result = num1 * num2
            elif operation == 'DIV':
                if num2 == 0:
                    return render(request, 'calci/index.html', {'error': 'Cannot divide by zero!'})
                result = num1 / num2
            
            # Round long decimal results
            if isinstance(result, float):
                result = round(result, 4)
                
            return render(request, 'calci/index.html', {'result': result, 'num1': num1, 'num2': num2})
            
        except Exception as e:
            return render(request, 'calci/index.html', {'error': 'An error occurred!'})

    return HttpResponse("Invalid request")