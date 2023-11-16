from django.shortcuts import redirect, render

from .functions.auth import create_user_profile, validate_credentials

# Create your views here.
def home_view(request):
    page_header = "Home"
    context = {"page_header": page_header}
    return render(request, "user_interface/home.html", context)

def register_view(request):
    
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

