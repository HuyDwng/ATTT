from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
urlpatterns = [
    path('',views.get_home,name='tour_management'),
    path('payment',views.get_payment, name='payment'),
    path('add_tour',views.get_add_tour,name='add_tour'),
    path('tour_edit',views.get_tour_edit, name='tour_edit'),
    path('revenue_statistics',views.get_revenue_statistics,name='revenue_statistics')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)