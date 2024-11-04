from django.shortcuts import render, redirect


# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Management.models import Users, Tour, Tickets, Booking, Payment
from django.contrib.auth.models import User
from django.contrib import messages


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


def members(request):
  context = get_common_context()
  return render(request, 'admin_tour/tour_list.html', context)
def create_group(request):
  context = get_common_context()
  return render(request, 'admin_tour/create_group.html', context)

def create_user(request):
  context = get_common_context()
  if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number') 
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
                    user_account = User.objects.create_user(username=username, email=email, password=password1)
                    user = Users.objects.create(username=username, email=email, password=password1, phone_number=phone_number, fullname=fullname)
                    user.save()
                    user_account.save()
                    messages.success(request, "Đăng ký thành công!")
                    return redirect('login')
            else:
                messages.error(request, "Mật khẩu không khớp")
  return render(request, 'admin_tour/create_user.html', context)

def group_management(request):
  context = get_common_context()
  return render(request, 'admin_tour/group_management.html', context)

def organized_tour(request):
  context = get_common_context()
  return render(request, 'admin_tour/organized_tour.html', context)

def tour_management(request):
  context = get_common_context()
  return render(request, 'admin_tour/tour_management.html', context)

def transaction_management(request):
  context = get_common_context()
  return render(request, 'admin_tour/transaction_management.html', context)

def user_management(request):
  context = get_common_context()
  return render(request, 'admin_tour/user_management.html', context)
