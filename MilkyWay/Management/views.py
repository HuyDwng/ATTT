from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render
from Management.utils import encrypt_data, decrypt_data
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count

# Function system
def decrypted_tours():
    tour = Tour.objects.all()
    tours_with_images = []
    for t in tour:
        images = t.images.all()  # Lấy tất cả hình ảnh liên quan đến tour
        decrypted_tour = {
            'id': t.id,
            'start_date': t.start_date,
            'end_date': t.end_date,
            'name': t.decrypted_data('name'),
            'description': t.decrypted_data('description'),
            'start_location': t.decrypted_data('start_location'),
            'destination': t.decrypted_data('destination'),
            'price': t.decrypted_data('price'),
            'available_seats': t.decrypted_data('available_seats'),
            'remaining_seats': t.decrypted_data('remaining_seats'),
            'images': images,
            'start_date': t.start_date,
            'end_date':t.end_date,
        }
        tours_with_images.append(decrypted_tour)
    return tours_with_images

def decrypted_user(request):
    users = Users.objects.all()
    return [
        {
            'id': t.id,
            'username': t.username,
            'password': t.decrypted_data('password'),
            'email': t.decrypted_data('email'),
            'fullname': t.decrypted_data('fullname'),
            'phone_number': t.decrypted_data('phone_number'),
            'role': t.role,
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
            'id': t.id,
            'tour': t.tour,
            'user': t.user,
            'status': t.status,
            'ticket_code': t.decrypted_data('ticket_code'),
            'payment_method': t.payment.payment_method if hasattr(t, 'payment') else "No payment method",
        }
        for t in bookings
    ]
def decrypted_payments():
    payments = Payment.objects.all()
    return [
        {
            'amount': t.decrypted_data('amount'),
            'payment_method': t.payment_method,
            'payment_state': t.payment_state,
        }
        for t in payments
    ]
def get_common_context(request):
    tours = decrypted_tours()
    users = decrypted_user(request)
    tickets = decrypted_tickets()
    bookings = decrypted_bookings()  
    payments = decrypted_payments()      
    try:
        current_user = request.session['username']
    except KeyError:
        current_user = None 
    return {
        'tour': tours,
        'user': users,
        'ticket': tickets,
        'booking':bookings,
        'payment': payments,
        'current_user': current_user
    }


def members(request):
    context = get_common_context(request)
    dates, counts = weekly_tour_purchases()
    context['date','counts'] =  dates, counts
    return render(request, 'admin_tour/tour_list.html', context)

def create_group(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/create_group.html', context)

def create_user(request):
  context = get_common_context(request)
  if request.method == 'POST':
        # Lấy dữ liệu từ form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['confirm_password']
        phone_number = request.POST.get('phone_number') 
        fullname = request.POST.get('fullname')
        role = request.POST.get('form-select')
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
                    if role == "admin":
                        user_account = User.objects.create_user(username=username, email=email, password=password1)
                        user = Users.objects.create(username=username, email=email, password=password1, phone_number=phone_number, fullname=fullname, role=role)
                        messages.success(request, "Đăng ký thành công!")
                    elif role == "staff" or role == "user":
                        user = Users.objects.create(username=username, email=email, password=password1, phone_number=phone_number, fullname=fullname, role=role)
                        messages.success(request, "Đăng ký thành công!")
                    else:
                       messages.error(request, "Vui lòng chọn vai trò")
            else:
                messages.error(request, "Mật khẩu không khớp")
  return render(request, 'admin_tour/create_user.html', context)

def group_management(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/group_management.html', context)

def organized_tour(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/organized_tour.html', context)

def tour_management(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/tour_management.html', context)

def transaction_management(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/transaction_management.html', context)

def user_management(request):
  context = get_common_context(request)
  return render(request, 'admin_tour/user_management.html', context)

def create_tour(request):
    if request.method == 'POST':
        # Nhận thông tin tour từ form
        name = request.POST.get('tour_name')
        start_location = request.POST.get('start_location')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        price = request.POST.get('tour_price')
        available_seats = request.POST.get('passenger_count')
        remaining_seats = available_seats

        # Thu thập mô tả địa điểm từ các trường itinerary_0, itinerary_1, ...
        descriptions = []
        for key in request.POST:
            if key.startswith('itinerary_'):
                descriptions.append(request.POST.get(key))
        
        description = '*'.join(descriptions)  # Ghép các mô tả lại với dấu `*` phân cách

        # Lưu thông tin Tour
        tour = Tour(
            name=name,
            description=description,
            start_location=start_location,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            price=price,
            available_seats=available_seats,
            remaining_seats=remaining_seats,
        )
        tour.save()

        # Lưu ảnh
        images = request.FILES.getlist('tour_image')
        for idx, image in enumerate(images):
            Images.objects.create(tour=tour, images=image, position=idx + 1)

        return redirect('tour_management')

    context = {'range': range(1, 5)}
    return render(request, 'admin_tour/create_tour.html', context)


def edit_user(request, user_id):
    context = get_common_context(request)
    user = get_object_or_404(Users, id=user_id)
    decrypted_user = {
            'id': user.id,  
            'username': user.username,
            'email': decrypt_data(user.email),
            'phone_number': decrypt_data(user.phone_number),
            'fullname': decrypt_data(user.fullname),
            'password': decrypt_data(user.password),
            'role': user.role,
        }
    
    if request.method == 'POST':
        user.name = request.POST.get('username')
        user.email = request.POST.get('email')
        user.password = request.POST.get('password')
        user.fullname = request.POST.get('fullname')
        user.phone_number = request.POST.get('phone_number')
        user.role = request.POST.get('form-select')
        user.save()
        return redirect('user_management')
    context['users'] = decrypted_user
    return render(request, 'admin_tour/edit_user.html', context)

def delete_user(request, user_id):
    context = get_common_context(request)
    user = get_object_or_404(Users, id=user_id)
    user.delete()
    return redirect('user_management')

def edit_tour(request, tour_id):
     # Lấy tour cần chỉnh sửa
    tour = get_object_or_404(Tour, id=tour_id)
    images = tour.images.all()
    decrypted_tour = {
            'id': tour.id,  
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'name': tour.decrypted_data('name'),
            'description': tour.decrypted_data('description'),
            'start_location': tour.decrypted_data('start_location'),
            'destination': tour.decrypted_data('destination'),
            'price': tour.decrypted_data('price'),
            'available_seats': tour.decrypted_data('available_seats'),
            'remaining_seats': tour.decrypted_data('remaining_seats'),
            'images': images,
            'start_date':tour.start_date.strftime("%Y-%m-%d") if tour.start_date else "",  
            'end_date':tour.end_date.strftime("%Y-%m-%d") if tour.end_date else "",
        }
    tours = decrypted_tours()
    images = Images.objects.filter(tour=tour)
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""

    if request.method == 'POST':
        # Cập nhật các thông tin tour từ form
        tour.name = request.POST.get('tour_name')
        tour.start_location = request.POST.get('start_location')
        tour.destination = request.POST.get('destination')
        tour.start_date = request.POST.get('start_date')
        tour.end_date = request.POST.get('end_date')
        tour.price = request.POST.get('tour_price')
        tour.available_seats = request.POST.get('passenger_count')
        tour.remaining_seats = request.POST.get('remaining_count')

        # Thu thập tất cả các mô tả từ form input `description[]`
        descriptions = request.POST.getlist('description[]')  # Sử dụng getlist để lấy tất cả mô tả
        tour.description = '*'.join(descriptions)  # Ghép các mô tả lại với dấu `*` phân cách

        # Lưu lại tour sau khi chỉnh sửa
        tour.save()

        return redirect('tour_management')  # Chuyển hướng về trang quản lý tour sau khi lưu

    # Nếu là GET, render form với dữ liệu hiện tại

    desc = tour.decrypted_description()
    descriptions = desc.split('*') if desc else []

    context = {
        'tours': decrypted_tour,
        'images': images,
        'descriptions': descriptions,
    }
    return render(request, 'admin_tour/edit_tour.html', context)

def delete_tour(request, tour_id):
    context = get_common_context(request)
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect('tour_management')

def delete_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)  # Tìm ảnh theo ID
    if request.method == 'POST':
        image.delete()  # Xóa ảnh khỏi database
        return redirect('edit_tour', tour_id=image.tour.id)  # Điều hướng trở lại trang chỉnh sửa tour

def add_images_admin(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        images = request.FILES.getlist('tour_images')  # Nhận danh sách file hình ảnh
        for img in images:
            Images.objects.create(tour=tour, images=img)  # Tạo đối tượng hình ảnh
            
        return redirect('edit_tour', tour_id=tour_id)  # Điều hướng lại trang chỉnh sửa tour
    
def change_image_admin(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    if request.method == 'POST':
        new_image = request.FILES.get('new_image')  # Nhận hình ảnh mới
        if new_image:
            image.images = new_image  # Thay đổi hình ảnh
            image.save()  # Lưu thay đổi
    return redirect('edit_tour', tour_id=image.tour.id)  # Điều hướng lại trang chỉnh sửa tour

def delete_transaction(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('transaction_management')

def weekly_tour_purchases():
    today = timezone.now().date()
    last_week = today - timedelta(days=6) 

    data = (
        Booking.objects.filter(booking_date__range=(last_week, today))
        .values('booking_date')
        .annotate(count=Count('id'))
        .order_by('booking_date')
    )
    
    dates = [entry['booking_date'] for entry in data]
    counts = [entry['count'] for entry in data]

    return dates, counts
