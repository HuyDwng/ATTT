from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("/signup", views.signup, name="sig-up"),
    path("/forget", views.forget, name="forget"),
]