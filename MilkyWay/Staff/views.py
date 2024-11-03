from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.shortcuts import get_object_or_404, render  

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


def get_home(request):  
    context = get_common_context()
    return render(request, 'tour_management/tour_mng.html', context)
def get_payment(request):
    context = get_common_context()
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

        return redirect('tour_management')

    context = {'range': range(1, 5)}
    return render(request, 'tour_management/add_tour.html', context)



def get_tour_edit(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    images = Images.objects.filter(tour=tour)  # Lấy các ảnh thuộc tour này
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""
   
    # Tách description thành danh sách, nếu description không rỗng
    descriptions = tour.description.split('*') if tour.description else []

    # Cập nhật context để bao gồm danh sách ảnh
    context = {
        'range': range(1, 5),
        'tour': tour,
        'images': images,  # Thêm danh sách ảnh vào context
        'user': user,
        'ticket': ticket,
        'booking': booking,
        'payment': payment,
        'descriptions': descriptions,  # Thêm danh sách mô tả vào context
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

def get_revenue_statistics(request):
    context = get_common_context()
    return render(request,'revenue_statistics/revenue_statistics.html',context)