from django.shortcuts import render, redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review, Images
from django.db.models import OuterRef, Subquery
from datetime import timedelta, datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from urllib.parse import urlencode
from django.db.models import Count

# Create your views here.
def index(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    tour_counts = Tour.objects.values('destination').annotate(count=Count('destination')).order_by('-count')
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review,'tour_counts': tour_counts}
    return render(request, 'index.html', context)

def payment(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'payment.html', context)

def hotel(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'hotel.html', context)

def confirm_payment(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'payment_confirm.html', context)

def guide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'saigonguide.html', context)

@csrf_exempt
def tour(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'tour.html', context)

def tour_detail(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'tour-detail.html', context)

def turkeyguide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
    return render(request, 'turkeyguide.html', context)

def saigonguide(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user': user, 'ticket': ticket, 'booking': booking, 'payment': payment, 'review': review}
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