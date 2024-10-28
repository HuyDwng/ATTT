from django.shortcuts import render, redirect
from Management.models import Users, Tour, Tickets, Booking, Payment, Review, Images

# Create your views here.
def get_home(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request, 'tour_management/tour_mng.html', context)
def get_payment(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request,'payment_mng/payment_mng.html', context)
def get_add_tour(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()

    # if request.method == 'POST':  
    #     section_count = len(request.POST) 
    #     description = ''
    #     tour_name = request.POST.get('tour_name')
    #     destination = request.POST.get('tour_location')
    #     price = request.POST.get('tour_guide')
    #     available_seats = request.POST('passenger_count')
    #     start_location = "SaiGon"
    #     start_date = "22/10/2024"
    #     end_date = "25/10/2024"
    #     for i in range(1, section_count + 1):
    #         itinerary_key = f'itinerary_{i}'
    #         itinerary = request.POST.get(itinerary_key)
    #         description += itinerary + '*'
    #     tours = Tour.objects.create(name=tour_name, description= description, start_location=start_location, destination=destination, start_date=start_date, end_date=end_date, price=price, available_seats=available_seats)
    #     tours.save()
    #     for i in range(1, section_count + 1):
    #         image_key = f'tour_image_{i}'
    #         if image_key in request.FILES:
    #             for file in request.FILES.getlist(image_key):
    #                 image=Images.objects.create(tour=tours, images=file, position=i)  
    #                 image.save()
    #     return redirect('tour_detail', tour_id=tour.id)  

    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request,'tour_management/add_tour.html', context)
def get_tour_edit(request):
    tour = Tour.objects.all()
    user = Users.objects.all()
    ticket = Tickets.objects.all()
    booking = Booking.objects.all()
    payment = Payment.objects.all()
    review = Review.objects.all()
    context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
    return render(request,'tour_management/tour_edit.html', context)