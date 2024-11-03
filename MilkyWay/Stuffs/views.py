from django.shortcuts import render, redirect, get_object_or_404
import os
from Management.models import Users, Tour, Tickets, Booking, Payment, Images
from django.db.models import OuterRef, Subquery


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


# Create your views here.

def index(request):
    context = get_common_context()
    return render(request, 'index.html', context)

def payment(request):
    context = get_common_context()
    return render(request, 'payment.html', context) 

def hotel(request):
    context = get_common_context()
    return render(request, 'hotel.html', context) 

def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Lấy thông tin đặt chỗ
    tour = booking.tour  # Lấy thông tin tour từ đặt chỗ

    if request.method == 'POST':
        if form.is_valid():
            # Lấy thông tin từ form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            payment_method = form.cleaned_data['payment_method']
            amount = tour.price  # Giả sử bạn có trường giá trong mô hình Tour

            # Tạo đối tượng Payment và lưu vào cơ sở dữ liệu
            payment = Payment(
                booking=booking,
                amount=amount,
                payment_method=payment_method,
                payment_state='successful'  # Cập nhật trạng thái thanh toán
            )
            payment.save()
            return redirect('payment_success')  # Chuyển hướng sau khi thanh toán thành công
    else:
        form = Payment()
    context = get_common_context()
    return render(request, 'payment_confirm.html', context)

def guide(request):
    context = get_common_context()
    return render(request, 'saigonguide.html', context) 

def tour(request):
    context = get_common_context()
    return render(request, 'tour.html', context) 

def tour_detail(request):
    context = get_common_context()
    return render(request, 'tour-detail.html', context) 

def turkeyguide(request):
    context = get_common_context()
    return render(request, 'turkeyguide.html', context)

def saigonguide(request):
    context = get_common_context()
    return render(request, 'saigonguide.html', context)