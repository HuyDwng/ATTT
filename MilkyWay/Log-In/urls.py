from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("login", views.login, name="login"),
    path("forget", views.forget, name="forget"),
    path('sign-out', views.sign_out, name='sign_out'),
    path('register', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)