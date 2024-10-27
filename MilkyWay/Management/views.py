from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from Management.models import Users, Tour, Tickets, Booking, Payment, Review 

def members(request):
  template = loader.get_template('tour_list.html')
  tour = Tour.objects.all()
  user = Users.objects.all()
  ticket = Tickets.objects.all()
  booking = Booking.objects.all()
  payment = Payment.objects.all()
  review = Review.objects.all()
  context = {'tour': tour, 'user':user, 'ticket':ticket, 'booking':booking, 'payment':payment, 'review':review}
  return HttpResponse(template.render(), context)