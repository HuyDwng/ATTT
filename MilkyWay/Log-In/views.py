from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def login(request):
    # Logic xử lý đăng nhập
    return render(request, 'log_in/log-in.html')

def sign_up(request):
    return render(request, 'log_in/sig-up.html') 
