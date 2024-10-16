from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def login(request):
    # Logic xử lý đăng nhập
    return render(request, 'log_in/log-in.html')

def signup(request):
    return render(request, 'log_in/sig-up.html') 

def forget(request):
    return render(request, 'log_in/forget-password.html') 
