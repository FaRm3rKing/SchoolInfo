from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib  import messages
from django.http import HttpResponseBadRequest
from .forms import CreateUserForm
import utils



def registration_page(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            form.save()
            user_data = {"email": data["email"],
                         "first_name":data["fname"],
                         "last_name":data["lname"],
                         "gender":data["gender"],
                        }
            database, _ = utils.get_db_client()
            if data['role'] == "student":
                collection = database["student"]
                utils.Student(collection, **user_data)
            elif data['role'] == "teacher":
                pass
            else:
                error_message = f"Invalid input: no such role as {data['role']}"
                return HttpResponseBadRequest(error_message)
            return redirect("login")
        else:
            for error in list(form.errors.values()):
                print(request, error)
    context = {'form': form }
    return render(request, "registration.html", context)

def login_page(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)
        # validate password
        if user is not None:
            redirect_page = {"student": "student_home", 
                             "teacher": "teacher_database"}
            login(request, user)
            return redirect(redirect_page[user.role])
        else:
            messages.error(request, 'Invalid  username or password')
    return render(request, "login.html")
