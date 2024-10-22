from django.shortcuts import render
import os

# Create your views here.
def index(request):
    return render(request, 'homepage/index.html')

def payment(request):
    return render(request, 'homepage/payment.html') 

def hotel(request):
    return render(request, 'homepage/hotel.html') 

def confirm_payment(request):
    return render(request, 'homepage/payment_confirm.html')

def guide(request):
    return render(request, 'homepage/saigonguide.html') 


