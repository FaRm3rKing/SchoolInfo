from . import views
from django.urls import path


urlpatterns = [
    path('database/', views.teacher_database, name="teacher_database"), # temporary default page for teacher
    path('attendance/', views.teacher_attendance, name="teacher_attendance"),
    path('dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    path('messenger/', views.teacher_messenger, name="teacher_messenger"),
    path('calendar/', views.teacher_calendar, name="teacher_calendar"),
    path('settings/', views.teacher_settings, name="teacher_settings"),
    path('database/add-student/', views.add_student, name="add_student"),
    path('database/delete-student/', views.delete_student, name="delete_student"),
    # path('signout/', views.signout, name="signout")
]
