from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('tour-list',views.members,name='tour-list'),
    path('create_group',views.create_group,name='create_group'),
    path('create_user',views.create_user,name='create_user'),
    path('group_management',views.group_management,name='group_management'),
    path('organized_tour',views.organized_tour,name='organized_tour'),
    path('tour_management',views.tour_management,name='tour_management'),
    path('transaction_management',views.transaction_management,name='transaction_management'),
    path('user_management',views.user_management,name='user_management'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)