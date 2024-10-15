from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("sig-up/", views.sign_up, name="sig-up"),
]