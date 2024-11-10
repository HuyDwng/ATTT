from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests
import os, json
from cryptography.fernet import Fernet
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from Management.models import Users, Tour, Tickets, Booking, Payment
from Management.utils import encrypt_data, decrypt_data
import datetime
from django.conf import settings

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
                if Users.objects.filter(username=username).exists():
                    messages.error(request, "Tên người dùng đã tồn tại")
                elif Users.objects.filter(email=email).exists():
                    messages.error(request, "Email đã được sử dụng")
                else:
                    # Tạo người dùng mới
                    # user_account = User.objects.create_user(username=username, email=email, password=password1)  __ tài khoản admin
                    user = Users(username=username, email=email, password=password, phone_number=phone_number, fullname=fullname)
                    user.save()
                    # user_account.save()
                    messages.success(request, "Đăng ký thành công!")
                    return redirect('login')
            else:
                messages.error(request, "Mật khẩu không khớp")
    return render(request, 'log_in/sign-up.html', context)


@csrf_exempt
def login(request):
    context = get_common_context()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username:
            messages.error(request, "Không được để trống tên đăng nhập")
        elif not password:
            messages.error(request, "Vui lòng nhập mật khẩu")
        else:
            # Tìm người dùng dựa trên tên đăng nhập
            try:
                fernet = Fernet(settings.FERNET_KEY)
                user = Users.objects.get(username=username)
                db_password = (user.decrypted_data('password'))
                if  db_password == password:
                    role = user.role.lower()
                    if role == "customer":
                        request.session['username'] = user.username
                        request.session['email'] = user.decrypted_data('email')
                        request.session['password'] = user.decrypted_data('password')
                        request.session['phone'] = user.decrypted_data('phone_number')
                        request.session['fullname'] = user.decrypted_data('fullname')
                        return redirect('homepage')  
                    elif role == "staff":
                        request.session['username'] = user.username
                        return redirect('tour_mng')
                    elif role == "admin":
                        request.session['username'] = user.username
                        return redirect('tour-list')
                    else:
                        messages.error(request, "Lỗi phân quyền người dùng")
                else:
                    messages.error(request, "Mật khẩu không chính xác")
            except Users.DoesNotExist:
                messages.error(request, "Tên đăng nhập không tồn tại")
            except Exception as e:
                messages.error(request, "Đã xảy ra lỗi trong quá trình đăng nhập")
                print(e)

    return render(request, 'log_in/log_in.html', context)

@csrf_exempt
def forget(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        # Kiểm tra tính hợp lệ của dữ liệu
        if username == "":
            messages.error(request, "Không được để trống tên đăng nhập")
        else:
            if Users.objects.filter(username=username).exists():
                if password == password1:
                    user = Users.objects.get(username=username)
                    user.password = password
                    user.save()
                    messages.success(request, "Đổi mật khẩu thành công!")
                    return redirect('login')
                else:
                    messages.error(request, "Mật khẩu không khớp")                          
                    return redirect('forget')
            else:
                messages.error(request, "Tên người dùng không đã tồn tại")
    return render(request, 'log_in/forget-password.html') 

def sign_out(request):
    del request.session['username']
    del request.session['email']
    del request.session['password']
    del request.session['phone']
    del request.session['fullname']
    return redirect('login')

#Tài khoản google
# @csrf_exempt
# def auth_receiver(request):
#     if request.method == 'POST':
#         token = request.POST.get('credential')

#         try:
#             # Xác minh token Google
#             user_data = id_token.verify_oauth2_token(
#                 token, requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
#             )
#         except ValueError:
#             return JsonResponse({'error': 'Token không hợp lệ'}, status=403)

#         # Lấy email và thông tin người dùng từ Google
#         email = user_data.get('email')
#         username = email  # Sử dụng email làm username
#         password = email  # Sử dụng email làm password (nên mã hóa)

#         # Kiểm tra xem người dùng đã tồn tại trong hệ thống chưa
#         user, created = User.objects.get_or_create(username=username)

#         if created:
#             # Nếu tài khoản mới, thiết lập thêm thông tin người dùng
#             user.email = email
#             user.set_password(password)  # Đặt password là email (hoặc bạn có thể tạo mật khẩu tự sinh)
#             user.save()  # Lưu người dùng mới vào database

#         # Trả về phản hồi thành công và chuyển hướng
#         return JsonResponse({'message': 'Đăng nhập thành công'}, status=200)

#     return JsonResponse({'error': 'Yêu cầu không hợp lệ'}, status=400)

# def login_user(request):
    
#     return render(request, 'log_in/log-in.html')
