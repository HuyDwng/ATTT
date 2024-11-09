from django.shortcuts import render, redirect, get_object_or_404
import os, json
import os, json
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.db.models import OuterRef, Subquery
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.db.models import Count
from cryptography.fernet import Fernet
from django.conf import settings
from collections import Counter
from django.utils.dateparse import parse_date
from cryptography.fernet import Fernet
from django.conf import settings
from collections import Counter
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse

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
            'images': images,
            'start_date': t.start_date,
            'end_date': t.end_date,
            'duration_in_days_and_nights': t.duration_in_days_and_nights()
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
    # Lấy khóa Fernet từ settings
    fernet = Fernet(settings.FERNET_KEY)
    
    # Giải mã các tour và lưu các thông tin đã giải mã vào list
    decrypted_tours = []
    for tour in Tour.objects.all():
        decrypted_tour = {
            'id': tour.id,
            'name': json.loads(fernet.decrypt(tour.name.encode()).decode()),
            'description': json.loads(fernet.decrypt(tour.description.encode()).decode()),
            'start_location': json.loads(fernet.decrypt(tour.start_location.encode()).decode()),
            'destination': json.loads(fernet.decrypt(tour.destination.encode()).decode()),
            'price': json.loads(fernet.decrypt(tour.price.encode()).decode()),
            'available_seats': json.loads(fernet.decrypt(tour.available_seats.encode()).decode()),
            'remaining_seats': json.loads(fernet.decrypt(tour.remaining_seats.encode()).decode()),
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'images': tour.images.first(),  # Lấy hình ảnh đầu tiên của tour
            'duration_in_days_and_nights': tour.duration_in_days_and_nights()
        }
        decrypted_tours.append(decrypted_tour)
    
    # Đếm số lượng mỗi `destination` bằng Counter
    destinations = [tour['destination'] for tour in decrypted_tours]
    destination_counts = Counter(destinations)
    
    # Tạo danh sách `tour_counts` với các thông tin cần thiết
    tour_counts = []
    for dest, count in destination_counts.items():
        # Lấy tour đầu tiên với `destination` đã giải mã để lấy ảnh
        first_tour_with_dest = next((t for t in decrypted_tours if t['destination'] == dest), None)
        image_url = first_tour_with_dest['images'].ImageURL if first_tour_with_dest and first_tour_with_dest['images'] else None

        tour_counts.append({
            'destination': dest,
            'count': count,
            'image_url': image_url
        })

    # Sắp xếp danh sách theo số lượng giảm dần
    tour_counts.sort(key=lambda x: x['count'], reverse=True)

    # Thêm `tour_counts` vào context
    # Lấy khóa Fernet từ settings
    fernet = Fernet(settings.FERNET_KEY)
    
    # Giải mã các tour và lưu các thông tin đã giải mã vào list
    decrypted_tours = []
    for tour in Tour.objects.all():
        decrypted_tour = {
            'id': tour.id,
            'name': json.loads(fernet.decrypt(tour.name.encode()).decode()),
            'description': json.loads(fernet.decrypt(tour.description.encode()).decode()),
            'start_location': json.loads(fernet.decrypt(tour.start_location.encode()).decode()),
            'destination': json.loads(fernet.decrypt(tour.destination.encode()).decode()),
            'price': json.loads(fernet.decrypt(tour.price.encode()).decode()),
            'available_seats': json.loads(fernet.decrypt(tour.available_seats.encode()).decode()),
            'remaining_seats': json.loads(fernet.decrypt(tour.remaining_seats.encode()).decode()),
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'images': tour.images.first(),  # Lấy hình ảnh đầu tiên của tour
            'duration_in_days_and_nights': tour.duration_in_days_and_nights()
        }
        decrypted_tours.append(decrypted_tour)
    
    # Đếm số lượng mỗi `destination` bằng Counter
    destinations = [tour['destination'] for tour in decrypted_tours]
    destination_counts = Counter(destinations)
    
    # Tạo danh sách `tour_counts` với các thông tin cần thiết
    tour_counts = []
    for dest, count in destination_counts.items():
        # Lấy tour đầu tiên với `destination` đã giải mã để lấy ảnh
        first_tour_with_dest = next((t for t in decrypted_tours if t['destination'] == dest), None)
        image_url = first_tour_with_dest['images'].ImageURL if first_tour_with_dest and first_tour_with_dest['images'] else None

        tour_counts.append({
            'destination': dest,
            'count': count,
            'image_url': image_url
        })

    # Sắp xếp danh sách theo số lượng giảm dần
    tour_counts.sort(key=lambda x: x['count'], reverse=True)

    # Thêm `tour_counts` vào context
    context = get_common_context()
    context['tour_counts'] = tour_counts
    
    return render(request, 'index.html', context)
    context['tour_counts'] = tour_counts
    
    return render(request, 'index.html', context)

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
    remaining_seats = int(tour.decrypted_data('remaining_seats'))
    decrypted_tour = {
        'id': tour.id,
        'name': tour.decrypted_data('name'),
        'description': tour.decrypted_data('description'),
        'start_location': tour.decrypted_data('start_location'),
        'destination': tour.decrypted_data('destination'),
        'price': tour.decrypted_data('price'),
        'available_seats': tour.decrypted_data('available_seats'),
        'remaining_seats': remaining_seats ,
        'images': images,
        'start_date': tour.start_date,
        'end_date': tour.end_date,
        'duration_in_days_and_nights': tour.duration_in_days_and_nights()
    }

    # Tách description thành hai phần dựa trên dấu '*'
    description_parts = decrypted_tour['description'].split('*', 1) if decrypted_tour['description'] else ["", ""]
    description_main = description_parts[0] if len(description_parts) > 0 else ""
    itinerary = description_parts[1] if len(description_parts) > 1 else ""

    tours = decrypted_tours()
    images = Images.objects.filter(tour=tour)
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""

    context.update({
        'tours': tours,
        'tour': decrypted_tour,
        'description_main': description_main,
        'itinerary': itinerary,
        'images': images,
    })
    return render(request, 'tour-detail.html', context)

def generate_ticket_code():
    import uuid
    return str(uuid.uuid4()).replace('-', '').upper()[:10]



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

    # Khởi tạo danh sách các tour đã giải mã
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []

    for tour in Tour.objects.all():
        decrypted_destination = json.loads(fernet.decrypt(tour.destination.encode()).decode())
        if decrypted_destination == destination:
            decrypted_tour = {
                'id': tour.id,
                'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
                'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
                'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
                'destination': decrypted_destination,
                'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
                'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
                'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
                'start_date': tour.start_date,
                'end_date': tour.end_date,
                'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
                'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
            }
            decrypted_tours.append(decrypted_tour)

    # Áp dụng bộ lọc tìm kiếm
    # Khởi tạo danh sách các tour đã giải mã
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []

    for tour in Tour.objects.all():
        decrypted_destination = json.loads(fernet.decrypt(tour.destination.encode()).decode())
        if decrypted_destination == destination:
            decrypted_tour = {
                'id': tour.id,
                'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
                'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
                'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
                'destination': decrypted_destination,
                'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
                'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
                'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
                'start_date': tour.start_date,
                'end_date': tour.end_date,
                'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
                'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
            }
            decrypted_tours.append(decrypted_tour)

    # Áp dụng bộ lọc tìm kiếm
    if starting_location:
        decrypted_tours = [tour for tour in decrypted_tours if starting_location.lower() in tour['start_location'].lower()]
        decrypted_tours = [tour for tour in decrypted_tours if starting_location.lower() in tour['start_location'].lower()]
    if destination:
        decrypted_tours = [tour for tour in decrypted_tours if destination.lower() in tour['destination'].lower()]
        decrypted_tours = [tour for tour in decrypted_tours if destination.lower() in tour['destination'].lower()]
    if start_date:
        try:
            start_date_obj = parse_date(start_date)
            if start_date_obj:
                decrypted_tours = [tour for tour in decrypted_tours if tour['start_date'] == start_date_obj]
        except ValueError:
            pass
        try:
            start_date_obj = parse_date(start_date)
            if start_date_obj:
                decrypted_tours = [tour for tour in decrypted_tours if tour['start_date'] == start_date_obj]
        except ValueError:
            pass
    if duration:
        try:
            duration_days = int(duration)
            decrypted_tours = [tour for tour in decrypted_tours if (tour['end_date'] - tour['start_date']).days >= duration_days]
        except ValueError:
            pass
        try:
            duration_days = int(duration)
            decrypted_tours = [tour for tour in decrypted_tours if (tour['end_date'] - tour['start_date']).days >= duration_days]
        except ValueError:
            pass
    if members:
        try:
            member_count = int(members)
            decrypted_tours = [tour for tour in decrypted_tours if tour['remaining_seats'] >= member_count]
        except ValueError:
            pass
        try:
            member_count = int(members)
            decrypted_tours = [tour for tour in decrypted_tours if tour['remaining_seats'] >= member_count]
        except ValueError:
            pass
    if price_range:
        if price_range == "low":
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] < 1000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] < 1000000]
        elif price_range == "medium":
            decrypted_tours = [tour for tour in decrypted_tours if 1000000 <= tour['price'] <= 2000000]
            decrypted_tours = [tour for tour in decrypted_tours if 1000000 <= tour['price'] <= 2000000]
        elif price_range == "rather":
            decrypted_tours = [tour for tour in decrypted_tours if 2000000 < tour['price'] <= 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if 2000000 < tour['price'] <= 4000000]
        elif price_range == "high":
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] > 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] > 4000000]

    # Sử dụng Paginator để phân trang
    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Chuẩn bị các tham số tìm kiếm cho phân trang
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = urlencode(query_params)

    return render(request, "tour.html", {
        "page_obj": page_obj,
        "query_string": query_string,
    })
def all_tours(request):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []
    for tour in Tour.objects.all():
        decrypted_tour = {
            'id': tour.id,
            'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
            'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
            'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
            'destination': fernet.decrypt(tour.destination.encode()).decode().strip('"'),
            'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
            'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
            'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
            'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
        }
        decrypted_tours.append(decrypted_tour)

    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tour.html", {
        "page_obj": page_obj,
    })
def tours_by_destination(request, destination):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []
    
    for tour in Tour.objects.all():
        decrypted_destination = json.loads(fernet.decrypt(tour.destination.encode()).decode())
        if decrypted_destination == destination:
            decrypted_tour = {
            'id': tour.id,
            'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
            'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
            'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
            'destination': fernet.decrypt(tour.destination.encode()).decode().strip('"'),
            'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
            'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
            'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
            'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
            }
            decrypted_tours.append(decrypted_tour)

    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tour.html", {
        "page_obj": page_obj,
    })
    return render(request, "tour.html", {
        "page_obj": page_obj,
        "query_string": query_string,
    })
def all_tours(request):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []
    for tour in Tour.objects.all():
        decrypted_tour = {
            'id': tour.id,
            'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
            'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
            'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
            'destination': fernet.decrypt(tour.destination.encode()).decode().strip('"'),
            'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
            'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
            'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
            'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
        }
        decrypted_tours.append(decrypted_tour)

    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tour.html", {
        "page_obj": page_obj,
    })
def tours_by_destination(request, destination):
    fernet = Fernet(settings.FERNET_KEY)
    decrypted_tours = []
    
    for tour in Tour.objects.all():
        decrypted_destination = json.loads(fernet.decrypt(tour.destination.encode()).decode())
        if decrypted_destination == destination:
            decrypted_tour = {
            'id': tour.id,
            'name': fernet.decrypt(tour.name.encode()).decode().strip('"'),
            'description': fernet.decrypt(tour.description.encode()).decode().strip('"'),
            'start_location': fernet.decrypt(tour.start_location.encode()).decode().strip('"'),
            'destination': fernet.decrypt(tour.destination.encode()).decode().strip('"'),
            'price': int(fernet.decrypt(tour.price.encode()).decode().strip('"').strip()),
            'available_seats': int(fernet.decrypt(tour.available_seats.encode()).decode().strip('"').strip()),
            'remaining_seats': int(fernet.decrypt(tour.remaining_seats.encode()).decode().strip('"').strip()) if tour.remaining_seats else 0,
            'start_date': tour.start_date,
            'end_date': tour.end_date,
            'tour_obj': tour,  # Giữ lại đối tượng tour để truy xuất sau
            'first_image_url': tour.images.first().images.url if tour.images.exists() else None  # Truy xuất URL hình ảnh đầu tiên
            }
            decrypted_tours.append(decrypted_tour)

    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "tour.html", {
        "page_obj": page_obj,
    })
    return render(request, "tour.html", {"page_obj": page_obj, "query_string": query_string})


@csrf_exempt
def book_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    decrypted_remaining_seats = tour.decrypted_data('remaining_seats')
    print(decrypted_remaining_seats)
    remaining_seats = int(decrypted_remaining_seats)
    print(remaining_seats)
    images = tour.images.all()
    decrypted_tour = {
        'id': tour.id,
        'name': tour.decrypted_data('name'),
        'description': tour.decrypted_data('description'),
        'start_location': tour.decrypted_data('start_location'),
        'destination': tour.decrypted_data('destination'),
        'price': tour.decrypted_data('price'),
        'available_seats': tour.decrypted_data('available_seats'),
        'remaining_seats': remaining_seats,
        'images': images,
        'start_date': tour.start_date,
        'end_date': tour.end_date,
        'duration_in_days_and_nights': tour.duration_in_days_and_nights()
    }
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, "Số lượng vé phải lớn hơn 0.")
            return redirect('tour_detail', tour_id=tour_id)
        
        if quantity > remaining_seats:
            messages.error(request, "Số vé đặt vượt quá số chỗ còn lại.")
            return redirect('tour_detail', tour_id=tour_id)
        
        if remaining_seats >= quantity:
            remaining_seats -= quantity
        tour.save()
        
        username = request.session.get('username')
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return HttpResponse("Bạn chưa đăng nhập", status=403)


        with transaction.atomic():
            # Tạo Booking
            ticket_code = generate_ticket_code()
            booking = Booking.objects.create(
                user=user,
                tour=tour,
                status='booked',
                ticket_code=ticket_code
            )
            
            # Tạo Tickets
            Tickets.objects.create(
                booking=booking,
                ticket_code=ticket_code,
                quantity=quantity,
                ticket_status='issued'
            )
            
            messages.success(request, "Đặt tour thành công!")
            return redirect('tour_detail', tour_id=tour_id)
    return render(request, 'tour_detail.html', {'tour': decrypted_tour})

def generate_ticket_code():
    import uuid
    return str(uuid.uuid4()).replace('-', '').upper()[:10]