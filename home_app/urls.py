from . import views
from django.urls import path


urlpatterns = [
    path("", views.login_page, name="login"),
    path("registration/", views.registration_page, name="register"),
]
