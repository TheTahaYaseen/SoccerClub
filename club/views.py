from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Address, UserProfile

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
            error, user = create_user_profile(username, email, phone_number, password)

            if not error:
                login(request, user=user)
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
                error = "An Error Occured During Login! Credentials Maybe Incorrect!"

    context = {"page_header": page_header, "error": error, 
               "username": username, "password": password}

    return render(request, "auth/login.html", context)

def logout_view(request):

    if request.user.is_authenticated:
        logout(request)

    previous_page = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_page)

@login_required(login_url="login")
def settings_view(request):

    page_header = "Settings"
    error = ""

    user = request.user
    user_profile = UserProfile.objects.get(associated_user = user)

    username = user.username
    email = user_profile.email
    phone_number = user_profile.phone_number    

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")

        user.username = username
        user_profile.email = email
        user_profile.phone_number = phone_number
        user.save()
        user_profile.save()

    addresses = user_profile.addresses.all()

    context = {"page_header": page_header, "error": error, "addresses": addresses,
               "username": username, "email": email, "phone_number": phone_number}
    
    return render(request, "auth/settings.html", context)

def add_address_view(request):
    page_header = "Add Address"
    error = ""

    if request.method == "POST":
        description = request.POST.get("description")
        suite_or_pobox = request.POST.get("suite_or_pobox")
        building = request.POST.get("building")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")

        fields = [description, suite_or_pobox, building, street, city, state, postal_code, country]
        if None in fields:
            error = "Please Donot Leave Any Field Empty!"

        if not error:
            address = Address.objects.create(
                description=description, suite_or_pobox=suite_or_pobox, building=building, 
                street=street, city=city, state=state, postal_code=postal_code, country=country
            )
            user = request.user
            user_profile = UserProfile.objects.get(associated_user=user)
            user_profile.addresses.add(address)
            previous_page = request.META.get('HTTP_REFERER', '/')
            return redirect(previous_page)

    context = {"page_header": page_header, "error": error}
    return render(request, "auth/address_form.html", context)