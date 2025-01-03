from django.shortcuts import render,redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.shortcuts import get_object_or_404, render  
from Management.utils import encrypt_data, decrypt_data
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
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
        }
        for t in tickets
    ]

def decrypted_bookings():
    booking = Booking.objects.all()
    return [
        {
            'id': t.id,
            'booking_date': t.booking_date,
            'tour': t.tour,
            'user': t.user,
            'status': t.status,
            'ticket_code': t.decrypted_data('ticket_code'),
            'payment_method': t.payment.payment_method if hasattr(t, 'payment') else "No payment method",
            'tickets': [
                {
                    'quantity': int(decrypt_data(ticket.quantity)),
                    'amount': int(decrypt_data(ticket.quantity)) * int(decrypt_data(t.tour.price)),
                }
                for ticket in t.ticket.all()
            ],
            'price': t.tour.price 
        }
        for t in booking
    ]
def decrypted_payments():
    payments = Payment.objects.all()
    return [
        {
            'amount': t.decrypted_data('amount'),
        }
        for t in payments
    ]
def get_common_context(request):
    tours = decrypted_tours()
    users = decrypted_user()
    tickets = decrypted_tickets()
    bookings = decrypted_bookings()  
    payments = decrypted_payments()
    images = Images.objects.all()      
    return {
        'tour': tours,
        'user': users,
        'ticket': tickets,
        'booking':bookings,
        'payment': payments,
        'image': images,
    }


# Đảm bảo người dùng phải đăng nhập mới vào được view này
def get_home(request):  
    if 'username' not in request.session:
        messages.error(request, "Vui lòng đăng nhập để vào staff.")
        return redirect('login') 
    context = get_common_context(request)
    context['current_user'] =request.session.get('username')
    
    context['current_email'] =decrypt_data(request.session.get('email'))

    return render(request, 'tour_management/tour_mng.html', context)
def get_payment(request):
    context = get_common_context(request)
    context['current_user'] =request.session.get('username')
    context['current_email'] =decrypt_data(request.session.get('email'))
    return render(request,'payment_mng/payment_mng.html', context)



def get_add_tour(request):
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

        return redirect('tour_mng')

    context = {'range': range(1, 5)}
    return render(request, 'tour_management/add_tour.html', context)



def get_tour_edit(request, tour_id):
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

        return redirect('tour_mng')  # Chuyển hướng về trang quản lý tour sau khi lưu

    # Nếu là GET, render form với dữ liệu hiện tại

    desc = tour.decrypted_description()
    descriptions = desc.split('*') if desc else []

    context = {
        'tour': decrypted_tour,
        'images': images,
        'descriptions': descriptions,
    }

    return render(request, 'tour_management/tour_edit.html', context)


    

    
def delete_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)  # Tìm ảnh theo ID
    if request.method == 'POST':
        image.delete()  # Xóa ảnh khỏi database
        return redirect('tour_edit', tour_id=image.tour.id)  # Điều hướng trở lại trang chỉnh sửa tour

def add_images(request, tour_id):
    if request.method == 'POST':
        tour = get_object_or_404(Tour, id=tour_id)
        images = request.FILES.getlist('tour_images')  # Nhận danh sách file hình ảnh
        for img in images:
            Images.objects.create(tour=tour, images=img)  # Tạo đối tượng hình ảnh
            
        return redirect('tour_edit', tour_id=tour_id)  # Điều hướng lại trang chỉnh sửa tour
    
def change_image(request, image_id):
    image = get_object_or_404(Images, id=image_id)
    if request.method == 'POST':
        new_image = request.FILES.get('new_image')  # Nhận hình ảnh mới
        if new_image:
            image.images = new_image  # Thay đổi hình ảnh
            image.save()  # Lưu thay đổi
    return redirect('tour_edit', tour_id=image.tour.id)  # Điều hướng lại trang chỉnh sửa tour

def delete_tour(request, tour_id):
    # Lấy đối tượng tour cần xóa từ database
    tour = get_object_or_404(Tour, id=tour_id)
    
    # Xóa tour khỏi database
    tour.delete()
    
    # Điều hướng trở lại trang quản lý tour sau khi xóa
    return redirect('tour_mng')

def get_revenue_statistics(request):
    context = get_common_context(request)
    # Lấy tất cả các bookings
    
    
    return render(request,'revenue_statistics/revenue_statistics.html',context)

def get_booking(request):
    context = get_common_context(request)
    context['current_user'] =request.session.get('username')
    
    context['current_email'] =decrypt_data(request.session.get('email'))
    return render(request,"booking_mng/booking_mng.html",context)

def ticket_details(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Lấy booking theo ID
    tickets = Tickets.objects.filter(booking=booking)  # Lấy tất cả vé liên quan đến booking này
    decrypted_tickets_list = [
        {
            'ticket_code': t.decrypted_data('ticket_code'),
            'quantity': t.decrypted_data('quantity'),
            'ticket_status': t.ticket_status,
        }
        for t in tickets
    ]
  
    return render(request, 'ticket_mng/ticket_details.html', {'booking': booking, 'tickets': decrypted_tickets_list})


def transaction_filter(request):
    transaction_id = request.GET.get('transaction_id', '')
    transaction_date = request.GET.get('transaction_date', '')
    transaction_status = request.GET.get('transaction_status', '')
   

    # Start with all bookings
    bookings = Booking.objects.all()

    # Apply filters based on the user's input
    if transaction_id:
        bookings = bookings.filter(id__icontains=transaction_id)
    
    if transaction_date:
        bookings = bookings.filter(booking_date=transaction_date)
    
    if transaction_status:
        bookings = bookings.filter(status=transaction_status)
    

    # Return the filtered results to the template
    return render(request, 'payment_mng/payment_mng.html', {'booking': bookings})
