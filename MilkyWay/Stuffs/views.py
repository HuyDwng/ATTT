from django.shortcuts import render
import os

# Create your views here.
def index(request):
    return render(request, 'index.html')

def payment(request):
    return render(request, 'payment.html') 

def hotel(request):
    return render(request, 'hotel.html') 

def confirm_payment(request):
    return render(request, 'payment_confirm.html')

def guide(request):
    return render(request, 'saigonguide.html') 


