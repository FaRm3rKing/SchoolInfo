from . import views
from django.urls import path


urlpatterns = [
    path("home/", views.student_home, name="student_home"),
    path("work/", views.student_work, name="student_work"),
    path("support/", views.student_support, name="student_support"),
    path("settings/", views.student_settings, name="student_settings"),
    path("profile/", views.student_profile, name="student_profile") ,
    path("profile/edit-profile", views.edit_profile, name="edit_profile") ,
    path("signout/", views.signout, name="signout") 
]


