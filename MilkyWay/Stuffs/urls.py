from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"),
    path("hotel", views.hotel, name="hotel"),
    path("payment", views.payment, name="payment"),
    path('guide', views.guide, name='guide'),
    path('confirm-payment', views.confirm_payment, name='confirm-payment'),
    path('tour', views.tour, name='tour'),
    path('tour_detail', views.tour_detail, name='tour_detail'),
]
