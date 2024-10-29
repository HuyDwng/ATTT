from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 

def members(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/tour_list.html', context)
def create_group(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/create_group.html', context)

def create_user(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/create_user.html', context)

def group_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/group_management.html', context)

def organized_tour(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/organized_tour.html', context)

def tour_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/tour_management.html', context)

def transaction_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/transaction_management.html', context)

def user_management(request):
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return render(request, 'admin_tour/user_management.html', context)
