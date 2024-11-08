from django.shortcuts import render, redirect, get_object_or_404
import os
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.db.models import OuterRef, Subquery
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.db.models import Count

# Function system
def decrypted_tours():
    tour = Tour.objects.all()
    tours_with_images = []
    for t in tour:
        images = t.images.all()  # Lấy tất cả hình ảnh liên quan đến tour
        decrypted_tour = {
            'id': t.id,
            'name': t.decrypted_data('name'),
            'description': t.decrypted_data('description'),
            'start_location': t.decrypted_data('start_location'),
            'destination': t.decrypted_data('destination'),
            'price': t.decrypted_data('price'),
            'available_seats': t.decrypted_data('available_seats'),
            'remaining_seats': t.decrypted_data('remaining_seats'),
            'images': images  
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
    bookings = Booking.objects.all()
    return [
        {
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
        }
        for t in payments
    ]
def get_common_context():
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


# Create your views here.
def index(request):
    context = get_common_context()
    tour_counts = Tour.objects.values('destination').annotate(count=Count('destination')).order_by('-count')
    return render(request, 'index.html', context )

def payment(request):
    context = get_common_context()
    return render(request, 'payment.html', context)

def hotel(request):
    context = get_common_context()
    return render(request, 'hotel.html', context)

def confirm_payment(request):
#     booking = get_object_or_404(Booking, id=booking_id)  # Lấy thông tin đặt chỗ
#     tour = booking.tour  # Lấy thông tin tour từ đặt chỗ

#     if request.method == 'POST':
#         if form.is_valid():
#             # Lấy thông tin từ form
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             payment_method = form.cleaned_data['payment_method']
#             amount = tour.price  # Giả sử bạn có trường giá trong mô hình Tour

#             # Tạo đối tượng Payment và lưu vào cơ sở dữ liệu
#             payment = Payment(
#                 booking=booking,
#                 amount=amount,
#                 payment_method=payment_method,
#                 payment_state='successful'  # Cập nhật trạng thái thanh toán
#             )
#             payment.save()
#             return redirect('payment_success')  # Chuyển hướng sau khi thanh toán thành công
#     else:
    # form = Payment()
    context = get_common_context()
    return render(request, 'payment_confirm.html', context)

def guide(request):
    context = get_common_context()
    return render(request, 'saigonguide.html', context)

@csrf_exempt
def tour(request):
    context = get_common_context()
    return render(request, 'tour.html', context)

def tour_detail(request, tour_id):
    context = get_common_context()
    # Lấy tour cần chỉnh sửa
    tour = get_object_or_404(Tour, id=tour_id)
    images = tour.images.all() 
    decrypted_tour = {
            'id': tour.id,
            'name': tour.decrypted_data('name'),
            'description': tour.decrypted_data('description'),
            'start_location': tour.decrypted_data('start_location'),
            'destination': tour.decrypted_data('destination'),
            'price': tour.decrypted_data('price'),
            'available_seats': tour.decrypted_data('available_seats'),
            'remaining_seats': tour.decrypted_data('remaining_seats'),
            'images': images  
        }
    tours = decrypted_tours()
    images = Images.objects.filter(tour=tour)
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""
    context = {
        'tours': tours,
        'tour': decrypted_tour,
        'images': images,
    }

    return render(request, 'tour-detail.html', context)

def turkeyguide(request):
    context = get_common_context()
    return render(request, 'turkeyguide.html', context)

def saigonguide(request):
    context = get_common_context()
    return render(request, 'saigonguide.html', context)

@csrf_exempt
def search_tours(request):
    if request.method == "POST":
        # Lấy dữ liệu từ form tìm kiếm
        starting_location = request.POST.get('starting_location')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        duration = request.POST.get('duration')
        members = request.POST.get('members')
        price_range = request.POST.get('price_range')

        # Tạo URL với các tham số GET
        url = f"/search_tours/?starting_location={starting_location}&destination={destination}&start_date={start_date}&duration={duration}&members={members}&price_range={price_range}"
        return redirect(url)

    # Nếu là GET, lấy các tham số từ URL
    starting_location = request.GET.get('starting_location')
    destination = request.GET.get('destination')
    start_date = request.GET.get('start_date')
    duration = request.GET.get('duration')
    members = request.GET.get('members')
    price_range = request.GET.get('price_range')

    # Lọc các tour dựa trên các tham số tìm kiếm
    tours = Tour.objects.all()
    if starting_location:
        tours = tours.filter(start_location__icontains=starting_location)
    if destination:
        tours = tours.filter(destination__icontains=destination)
    if start_date:
        tours = tours.filter(start_date=datetime.strptime(start_date, '%Y-%m-%d'))
    if duration:
        end_date = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=int(duration))
        tours = tours.filter(end_date__gte=end_date)
    if members:
        tours = tours.filter(remaining_seats__gte=int(members))
    if price_range:
        if price_range == "low":
            tours = tours.filter(price__lt=1000000)
        elif price_range == "medium":
            tours = tours.filter(price__gte=1000000, price__lte=2000000)
        elif price_range == "rather":
            tours = tours.filter(price__gt=2000000, price__lte=4000000)
        elif price_range == "high":
            tours = tours.filter(price__gt=4000000)

    # Sử dụng Paginator để phân trang
    paginator = Paginator(tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Chuẩn bị các tham số tìm kiếm cho phân trang
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params)

    return render(request, "tour.html", {"page_obj": page_obj, "query_string": query_string})