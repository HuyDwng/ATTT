from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import os, json, stripe
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from Management.utils import encrypt_data, decrypt_data
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
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import authenticate
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
    context = get_common_context(request)
    context['tour_counts'] = tour_counts
    context['current_user'] = request.session.get('username')

    return render(request, 'index.html', context)
    context['tour_counts'] = tour_counts
    
    return render(request, 'index.html', context)
    context['tour_counts'] = tour_counts
    
    return render(request, 'index.html', context)

def payment(request):
    context = get_common_context(request)
    return render(request, 'payment.html', context)

def hotel(request):
    context = get_common_context(request)
    return render(request, 'hotel.html', context)


def guide(request):
    context = get_common_context(request)
    return render(request, 'saigonguide.html', context)

@csrf_exempt
def tour(request):
    context = get_common_context(request)
    return render(request, 'tour.html', context)
def tour_detail(request, tour_id):
    context = get_common_context(request)
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
        'remaining_seats': remaining_seats,
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
    images = tour.images.all()[:4]

    # Định dạng lại ngày bắt đầu và kết thúc
    tour.start_date = tour.start_date.strftime("%Y-%m-%d") if tour.start_date else ""
    tour.end_date = tour.end_date.strftime("%Y-%m-%d") if tour.end_date else ""

    # Cập nhật context với dữ liệu đã tách và giữ nguyên định dạng
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
    context = get_common_context(request)
    return render(request, 'turkeyguide.html', context)

def saigonguide(request):
    context = get_common_context(request)
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
        decrypted_tours = [tour for tour in decrypted_tours if starting_location.lower() in tour['start_location'].lower()]
    if destination:
        decrypted_tours = [tour for tour in decrypted_tours if destination.lower() in tour['destination'].lower()]
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
        try:
            member_count = int(members)
            decrypted_tours = [tour for tour in decrypted_tours if tour['remaining_seats'] >= member_count]
        except ValueError:
            pass
    if price_range:
        if price_range == "low":
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] < 1000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] < 1000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] < 1000000]
        elif price_range == "medium":
            decrypted_tours = [tour for tour in decrypted_tours if 1000000 <= tour['price'] <= 2000000]
            decrypted_tours = [tour for tour in decrypted_tours if 1000000 <= tour['price'] <= 2000000]
            decrypted_tours = [tour for tour in decrypted_tours if 1000000 <= tour['price'] <= 2000000]
        elif price_range == "rather":
            decrypted_tours = [tour for tour in decrypted_tours if 2000000 < tour['price'] <= 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if 2000000 < tour['price'] <= 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if 2000000 < tour['price'] <= 4000000]
        elif price_range == "high":
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] > 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] > 4000000]
            decrypted_tours = [tour for tour in decrypted_tours if tour['price'] > 4000000]

    # Sử dụng Paginator để phân trang
    paginator = Paginator(decrypted_tours, 6)  # Mỗi trang hiển thị tối đa 6 tour
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

def generate_ticket_code():
    import uuid
    return str(uuid.uuid4()).replace('-', '').upper()[:10]


@csrf_exempt
def book_tour(request, tour_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    tour = get_object_or_404(Tour, id=tour_id)
    decrypted_remaining_seats = tour.decrypted_data('remaining_seats')
    remaining_seats = int(decrypted_remaining_seats)

    decrypted_tour = {
        'id': tour.id,
        'name': tour.decrypted_data('name'),
        'description': tour.decrypted_data('description'),
        'start_location': tour.decrypted_data('start_location'),
        'destination': tour.decrypted_data('destination'),
        'price': tour.decrypted_data('price'),
        'available_seats': tour.decrypted_data('available_seats'),
        'remaining_seats': remaining_seats,
        'start_date': tour.start_date,
        'end_date': tour.end_date,
        'duration_in_days_and_nights': tour.duration_in_days_and_nights()
    }

    if request.method == 'POST':
        quantity = int(request.POST.get('number_of_tickets'))
        total_amount = (int(decrypted_tour['price']))
        if quantity <= 0:
            messages.error(request, "Số lượng vé phải lớn hơn 0.")
            return redirect('tour_detail', tour_id=tour_id)
        if quantity > remaining_seats:
            messages.error(request, "Số vé đặt vượt quá số chỗ còn lại.")
            return redirect('tour_detail', tour_id=tour_id)

        # Tạo session thanh toán Stripe
        success_url = request.build_absolute_uri(reverse('confirm_payment')) 
        cancel_url = request.build_absolute_uri(reverse('tour_detail', args=[tour_id]))  

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'vnd',
                    'product_data': {'name': decrypted_tour['name']},
                    'unit_amount': total_amount,
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )

        # Lưu tạm dữ liệu booking vào session
        request.session['temp_booking'] = {
            'tour_id': tour.id,
            'quantity': quantity,
            'total_amount': total_amount,
        }
        return redirect(checkout_session.url, code=303)
    return render(request, 'tour_detail.html', {'tour': decrypted_tour})

@csrf_exempt
def confirm_payment(request):
    temp_booking = request.session.get('temp_booking')
    if not temp_booking:
        messages.error(request, "Không tìm thấy thông tin đặt tour.")
        return redirect('homepage')

    tour_id = temp_booking['tour_id']
    quantity = temp_booking['quantity']
    total_amount = temp_booking['total_amount']
    tour = get_object_or_404(Tour, id=tour_id)

    decrypted_remaining_seats = tour.decrypted_data('remaining_seats')
    remaining_seats = int(decrypted_remaining_seats)

    if remaining_seats < quantity:
        messages.error(request, "Số lượng vé vượt quá số chỗ còn lại.")
        return redirect('tour_detail', tour_id=tour_id)

    if remaining_seats >= quantity:
        tour.remaining_seats = str(remaining_seats - quantity)
        tour.name = tour.decrypted_data('name')
        tour.description = tour.decrypted_data('description')
        tour.start_location = tour.decrypted_data('start_location')
        tour.destination = tour.decrypted_data('destination')
        tour.price = tour.decrypted_data('price')
        tour.available_seats = tour.decrypted_data('available_seats')
        tour.save()

    username = request.session.get('username')
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return HttpResponse("Bạn chưa đăng nhập", status=403)

    with transaction.atomic():
        ticket_code = generate_ticket_code()
        booking = Booking.objects.create(
            user=user,
            tour=tour,
            status='booked',
            ticket_code=ticket_code,
            booking_date = timezone.now().date()
        )
        total_amount = total_amount * quantity
        Payment.objects.create(
            booking=booking,
            amount = total_amount,
            payment_state = "successful"
        )
        for _ in range(quantity):
            Tickets.objects.create(
                booking=booking,
                ticket_code=ticket_code,
                quantity=1,
                ticket_status='issued'
            )
    del request.session['temp_booking']
    messages.success(request, "Đặt tour thành công!")
    return redirect('homepage')

@csrf_exempt
def info_user(request):
    if 'username' not in request.session:
        return redirect('login')

    # Lấy đối tượng người dùng hiện tại
    current_username = request.session.get('username', '')
    try:
        current_user = Users.objects.get(username=current_username)
    except Users.DoesNotExist:
        return redirect('login')

    bookings = Booking.objects.filter(user=current_user)
    decrypted_bookings_list = [
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
    context = get_common_context(request)
    context['bookings'] = decrypted_bookings_list

    context['current_user'] = current_user.username
    context['current_email'] = decrypt_data(current_user.email)
    context['current_phone'] = decrypt_data(current_user.phone_number)
    context['current_password'] = request.session.get('password', '')  # Password thường không lưu trong session, chỉ lấy ví dụ
    context['current_fullname'] = decrypt_data(current_user.fullname)
    context['bookings'] = decrypted_bookings_list


    return render(request, 'info_user.html', context)

@csrf_exempt
def change_number(request):
    if request.method == 'POST':
        phone_number = request.POST.get('Phone_number')
        current_username = request.session.get('username', '')

        try:
            current_user = Users.objects.get(username=current_username)
        except Users.DoesNotExist:
            return redirect('login')

        if phone_number:
            encrypted_phone = encrypt_data(phone_number)
            current_user.phone_number = encrypted_phone
            current_user.save()

            request.session['phone'] = phone_number

            messages.success(request, "Đổi số điện thoại thành công!")
            return redirect('info_user')
        else:
            messages.error(request, "Chưa nhập số điện thoại")
            return redirect('info_user')

    return render(request, 'info_user.html')

# def user_bookings(request):
#     username = request.session.get('username')
#     print("helo helo")
#     bookings = Booking.objects.filter(user=username)
#     for t in bookings:
#         print(t.id)
#     decrypted_bookings_list = [
#         {
#             'id': t.id,
#             'tour': t.tour,
#             'user': t.user,
#             'status': t.status,
#             'ticket_code': t.decrypted_data('ticket_code'),
#             'payment_method': t.payment.payment_method if hasattr(t, 'payment') else "No payment method",
#         }
#         for t in bookings
#     ]
#     context = get_common_context(request)
#     context['bookings'] = decrypted_bookings_list
#     return render(request, 'info_user.html', context)
