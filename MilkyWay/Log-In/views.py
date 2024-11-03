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
from Management.models import Users, Tour, Tickets, Booking, Payment
import datetime

# Create your views here.

# Function system
def decrypted_tours():
    tour = Tour.objects.all()
    return [
        {
            'name': t.decrypted_data('name'),
            'description': t.decrypted_data('description'),
            'star_location': t.decrypted_data('star_location'),
            'destination': t.decrypted_data('destination'),
            'price': t.decrypted_data('price'),
            'available_seats': t.decrypted_data('available_seats'),
            'remaining_seats': t.decrypted_data('remaining_seats'),
        }
        for t in tour
    ]

def decrypted_user():
    users = Users.objects.all()
    return [
        {
            'password': t.decrypted_data('password'),
            'email': t.decrypted_data('email'),
            'fullname': t.decrypted_data('fullname'),
            'phone_number': t.decrypted_data('phone_number'),
        }
        for t in users
    ]

def decrypted_tickets():
    tickets = Tickets.objects.all()
    return [
        {
            'ticket_code': t.decrypted_data('ticket_code'),
            'quantity': t.decrypted_data('quantity'),
            'ticket_status': t.decrypted_data('ticket_status'),
        }
        for t in tickets
    ]

def decrypted_bookings():
    bookings = Booking.objects.all()
    return [
        {
            'status': t.decrypted_data('status'),
            'payment_method': t.decrypted_data('payment_method'),
            'ticket_code': t.decrypted_data('ticket_code'),
        }
        for t in bookings
    ]
def decrypted_payments():
    payments = Payment.objects.all()
    return [
        {
            'amount': t.decrypted_data('amount'),
            'payment_method': t.decrypted_data('payment_method'),
            'payment_state': t.decrypted_data('payment_state'),
        }
        for t in payments
    ]
def get_common_context():
    tours = decrypted_tours()
    users = decrypted_user()
    tickets = decrypted_tickets()
    bookings = decrypted_bookings()  
    payments = decrypted_payments()      
    return {
        'tour': tours,
        'user': users,
        'ticket': tickets,
        'booking':bookings,
        'payment': payments,
    }




@csrf_exempt
def register(request):
    context = get_common_context()
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
