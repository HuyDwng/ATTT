from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("signup", views.signup, name="sig-up"),
    path("forget", views.forget, name="forget"),
    path('sign-out', views.sign_out, name='sign_out'),
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
]


