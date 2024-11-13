from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import delete_image, add_images_admin, change_image_admin
urlpatterns = [
    path('tour-list',views.members,name='tour-list'),
    path('create_group',views.create_group,name='create_group'),
    path('create_user',views.create_user,name='create_user'),
    path('group_management',views.group_management,name='group_management'),
    path('organized_tour',views.organized_tour,name='organized_tour'),
    path('tour_management',views.tour_management_admin,name='tour_management_admin'),
    path('transaction_management',views.transaction_management,name='transaction_management'),
    path('user_management',views.user_management,name='user_management'),
    path('create_tour',views.create_tour,name='create_tour'),
    path('edit_user/<int:user_id>/',views.edit_user,name='edit_user'),
    path('delete_user/<int:user_id>',views.delete_user,name='delete_user'),
    path('delete_tour/<int:tour_id>',views.delete_tour_admin,name='delete_tour_admin'),
    path('edit_tour/<int:tour_id>/',views.edit_tour,name='edit_tour'),
    path('management/tour/add_images/<int:tour_id>/', add_images_admin, name='add_images_admin'),
    path('management/image/change/<int:image_id>/', change_image_admin, name='change_image_admin'),
    path('management/delete_transaction/<int:booking_id>/', views.delete_transaction, name='delete_transaction'),
    path('managemant/transaction_filtering', views.transaction_filtering, name='transaction_filtering'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)