from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 
from django.contrib.auth.models import User
from django.contrib import messages

def members(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/tour_list.html', context)
def create_group(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/create_group.html', context)

def create_user(request):
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
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/group_management.html', context)

def organized_tour(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/organized_tour.html', context)

def tour_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/tour_management.html', context)

def transaction_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/transaction_management.html', context)

def user_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/user_management.html', context)
