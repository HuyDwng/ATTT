from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import os

# Create your views here.

@csrf_exempt
def login(request):
    # Logic xử lý đăng nhập
    return render(request, 'log_in/log-in.html')

def signup(request):
    return render(request, 'log_in/sig-up.html') 

def forget(request):
    return render(request, 'log_in/forget-password.html') 




@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    print('Inside')
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

  
    request.session['user_data'] = user_data

    return redirect('login')


def sign_out(request):
    del request.session['user_data']
    return redirect('login')

