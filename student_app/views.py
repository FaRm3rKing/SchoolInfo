from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
import utils
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from .forms import EditProfileForm
from datetime import datetime

def get_student_data(user):
    database, _ = utils.get_db_client()
    collection = database['students']
    student_data = collection.find_one({"email": user})

    # change date format to mm-dd-YYY
    formatted_date = student_data["birthday"].date()
    student_data["birthday"] = formatted_date

    return student_data

def student_role_check(user):
    STUDENT = "student"
    try:
        user.role
    except Exception:
        print(f"Error: {Exception}")

    return user.role == STUDENT

@login_required
@user_passes_test(student_role_check)
def student_home(request):
    student_data = get_student_data(request.user.email)
    context = { "student_data": student_data }
    return render(request, "student_app/home.html", context)

@login_required
@user_passes_test(student_role_check)
def student_work(request):
    student_data = get_student_data(request.user.email)
    context = { "student_data": student_data }
    return render(request, "student_app/work.html", context)

@login_required
@user_passes_test(student_role_check)
def student_support(request):
    student_data = get_student_data(request.user.email)
    context = { "student_data": student_data }
    return render(request, "student_app/support.html", context)

@login_required
@user_passes_test(student_role_check)
def student_settings(request):
    student_data = get_student_data(request.user.email)
    context = { "student_data": student_data }
    return render(request, "student_app/settings.html", context)

@login_required
@user_passes_test(student_role_check)
def student_profile(request):
    student_data = get_student_data(request.user.email)

    context = { "student_data": student_data }
    if request.method == "POST":
        pass
    return render(request, "student_app/profile.html", context)

@login_required
@user_passes_test(student_role_check)
def edit_profile(request):
    student_data = get_student_data(request.user.email)

    selected_keys = ['first_name', 'last_name', 'birthday', 'address', 'phone']
    new_dict = {key: student_data[key] for key in selected_keys if key in student_data}

    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = EditProfileForm(request.POST, initial=new_dict)
        # check whether it's valid:
        if form.is_valid():

            if form.has_changed():
                database,_ = utils.get_db_client()
                collection = database["students"]
                student = utils.Student.get(collection=collection, student_id=student_data['school_id'])
                student.update(form.cleaned_data)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse("student_profile"))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditProfileForm(initial=new_dict)

    context = {"student_data": student_data,
               "form": form}
    return render(request, "student_app/edit-profile.html", context=context)

def signout(request):
    logout(request)
    return redirect("login")


