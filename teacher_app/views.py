from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import utils

def teacher_role_check(user):
    TEACHER = "teacher"
    return user.role == TEACHER

@login_required
@user_passes_test(teacher_role_check)
def teacher_database(request):
    student_data = []
    database, _ = utils.get_db_client()

    if request.method == "POST":
        search = request.POST.get('query')
        database, _ = utils.get_db_client()

        if search:
            query = {"$or": [{"first_name": search }, {"last_name": search}] }
            student_data =  utils.read_db_data(collection_handle=database['students'],
                                               query=query,
                                               fields={})
        else:
            student_data =  utils.read_db_data(collection_handle=database['students'],fields={})

        page_context = {
            "student_data" : student_data
        }
        return render(request, 'teacher_app/database.html', context=page_context)

    student_data =  utils.read_db_data(collection_handle=database['students'],fields={})
    page_context = {
        "student_data" : student_data
    }
    return render(request, 'teacher_app/database.html', context=page_context)

@login_required
@user_passes_test(teacher_role_check)
def teacher_attendance(request):
    return render(request, 'teacher_app/attendance.html')

@login_required
@user_passes_test(teacher_role_check)
def teacher_dashboard(request):
    return render(request, 'teacher_app/dashboard.html')

@login_required
@user_passes_test(teacher_role_check)
def teacher_calendar(request):
    return render(request, 'teacher_app/calendar.html')

@login_required
@user_passes_test(teacher_role_check)
def teacher_messenger(request):
    return render(request, 'teacher_app/messenger.html')

@login_required
@user_passes_test(teacher_role_check)
def teacher_settings(request):
    return render(request, 'teacher_app/settings.html')

@login_required
@user_passes_test(teacher_role_check)
def add_student(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
    # USE save in Student class to save a student data
        database, _ = utils.get_db_client()
        collection = database["students"]
        student = utils.Student(collection=collection,
            first_name=fname, 
            last_name=lname, 
            email=email)
        student.save()
        return HttpResponseRedirect(reverse("teacher_database"))
    else:
        return HttpResponse(status=204)

@login_required
@user_passes_test(teacher_role_check)
def delete_student(request):
    if request.method == "POST":
        id = int(request.POST["student_id"])
        # USE save in Student class to save a student data
        database, _ = utils.get_db_client()
        collection = database["students"]
        student = utils.Student.get(collection=collection, student_id=id)
        if student is None:
            return HttpResponseBadRequest("Deletion did not succeed")
        student.delete()
        return HttpResponseRedirect(reverse("teacher_database"))
    else:
        return HttpResponse(status=204)
