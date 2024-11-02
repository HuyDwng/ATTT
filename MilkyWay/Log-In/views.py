from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests
import os
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 
import datetime

# Create your views here.


@csrf_exempt
def register(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        phone_number = request.POST.get('phone') 
        fullname = request.POST.get('fullname')
        # Kiểm tra tính hợp lệ của dữ liệu
        if username == "":
            messages.error(request, "Không được để trống tên đăng nhập")
        else:
            if password == password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Tên người dùng đã tồn tại")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email đã được sử dụng")
                else:
                    # Tạo người dùng mới
                    # user_account = User.objects.create_user(username=username, email=email, password=password1)  __ tài khoản admin
                    user = Users.objects.create(username=username, email=email, password=password1, phone_number=phone_number, fullname=fullname)
                    user.save()
                    # user_account.save()
                    messages.success(request, "Đăng ký thành công!")
                    return redirect('login')
            else:
                messages.error(request, "Mật khẩu không khớp")
    return render(request, 'log_in/sign-up.html', context)


@csrf_exempt
def login(request):
    return render(request, 'log_in/log-in.html')

def signup(request):
    return render(request, 'log_in/sign-up.html') 

def forget(request):
    return render(request, 'log_in/forget-password.html') 

def sign_out(request):
    del request.session['user_data']
    return redirect('login')
@csrf_exempt
def auth_receiver(request):
    if request.method == 'POST':
        token = request.POST.get('credential')

        try:
            # Xác minh token Google
            user_data = id_token.verify_oauth2_token(
                token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
            )
        except ValueError:
            return JsonResponse({'error': 'Token không hợp lệ'}, status=403)

        # Lấy email và thông tin người dùng từ Google
        email = user_data.get('email')
        username = email  # Sử dụng email làm username
        password = email  # Sử dụng email làm password (nên mã hóa)

        # Kiểm tra xem người dùng đã tồn tại trong hệ thống chưa
        user, created = User.objects.get_or_create(username=username)

        if created:
            # Nếu tài khoản mới, thiết lập thêm thông tin người dùng
            user.email = email
            user.set_password(password)  # Đặt password là email (hoặc bạn có thể tạo mật khẩu tự sinh)
            user.save()  # Lưu người dùng mới vào database

        # Trả về phản hồi thành công và chuyển hướng
        return JsonResponse({'message': 'Đăng nhập thành công'}, status=200)

    return JsonResponse({'error': 'Yêu cầu không hợp lệ'}, status=400)
