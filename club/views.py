from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate

from .functions.auth import create_user_profile, username_already_used, validate_credentials

# Create your views here.
def home_view(request):
    page_header = "Home"
    context = {"page_header": page_header}
    return render(request, "user_interface/home.html", context)

def register_view(request):
    
    if request.user.is_authenticated:
        return redirect("home")

    page_header = "Register"
    error = ""
    
    username = ""
    email = ""
    phone_number = ""
    password = ""
    password_confirmation = ""
    
    if request.method == "POST":
        
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        error = validate_credentials(username, email, phone_number, password, password_confirmation)

        if not error:
            error = create_user_profile(username, email, phone_number, password)

            if not error:
                return redirect("home")

    context = {"page_header": page_header, 
               "error": error, 
               "username": username, "email": email, "phone_number": phone_number, 
               "password": password, "password_confirmation": password_confirmation}

    return render(request, "auth/register.html", context)

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    error = ""
    page_header = "Login"

    username = ""
    password = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username_already_used(username):
            error = "User Does Not Exist!"
        else:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error = "An Error Occured During Login! Credential Maybe Incorrect!"

    context = {"page_header": page_header, "error": error, 
               "username": username, "password": password}
    return render(request, "auth/login.html", context)