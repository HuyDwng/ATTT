from django.shortcuts import render, redirect, get_object_or_404
import os
from Management.models import Users, Tour, Tickets, Booking, Payment, Review, Images
from django.db.models import OuterRef, Subquery

# Create your views here.
def index(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
     # Lấy tour và ảnh đầu tiên của mỗi tour (theo `position`)
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'index.html', context)

def payment(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'payment.html', context) 

def hotel(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
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
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'payment_confirm.html', context)

def guide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'saigonguide.html', context) 

def tour(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'tour.html', context) 

def tour_detail(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'tour-detail.html', context) 

def turkeyguide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'turkeyguide.html', context)

def saigonguide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'saigonguide.html', context)