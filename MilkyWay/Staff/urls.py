from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import delete_image, add_images, change_image

from . import views
urlpatterns = [
    path('',views.get_home,name='tour_mng'),
    path('payment',views.get_payment, name='payment'),
    path('add_tour',views.get_add_tour,name='add_tour'),
    path('booking_mng',views.get_booking,name='booking_mng'),
    path('tour/edit/<int:tour_id>/', views.get_tour_edit, name='tour_edit'),
    path('revenue_statistics',views.get_revenue_statistics,name='revenue_statistics'),
    path('image/delete/<int:image_id>/', delete_image, name='delete_image'),
    path('tour/add_images/<int:tour_id>/', add_images, name='add_images'),
    path('image/change/<int:image_id>/', change_image, name='change_image'),  # Thêm đường dẫn này
    path('delete_tour/<int:tour_id>/', views.delete_tour, name='delete_tour'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)