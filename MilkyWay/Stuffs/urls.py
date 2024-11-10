from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="homepage"),
    path("saigonguide", views.saigonguide, name="saigonguide"),
    path("turkeyguide", views.turkeyguide, name="turkeyguide"),
    path("hotel", views.hotel, name="hotel"),
    path("payment", views.payment, name="payment"),
    path('guide', views.guide, name='guide'),
    path('confirm_payment', views.confirm_payment, name='confirm_payment'),
    path('tour', views.tour, name='tour'),
    path('tour/tour_detail/<int:tour_id>/', views.tour_detail, name='tour_detail'),
    path('search_tours/', views.search_tours, name='search_tours'),
    path('all_tours/', views.all_tours, name='all_tours'),
    path('tours/<str:destination>/', views.tours_by_destination, name='tours_by_destination'),
    path('tour/tour_detail/<int:tour_id>/book/', views.book_tour, name='book_tour'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
