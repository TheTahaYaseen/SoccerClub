from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

    if request.user.is_superuser:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)

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

    context = {"page_header": page_header, "credentials_error": error, "addresses": addresses,
               "username": username, "email": email, "phone_number": phone_number}
    
    return render(request, "auth/settings.html", context)

@login_required(login_url="login")
def add_address_view(request):
    
    if request.user.is_superuser:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)

    page_header = "Add Address"
    error = ""
    action = "Add"

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
            return redirect("settings")

    context = {"page_header": page_header, "error": error, "action": action,
               "description": description, "suite_or_pobox": suite_or_pobox, "building": building, 
               "street": street, "city": city, "state": state, "postal_code": postal_code, "country": country}
    return render(request, "auth/address_form.html", context)

@login_required(login_url="login")
def update_address_view(request, primary_key):
    
    if request.user.is_superuser:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)

    page_header = "Update Address"
    error = ""
    action = "Update"
    address = Address.objects.get(id=primary_key)

    description = address.description
    suite_or_pobox = address.suite_or_pobox
    building = address.building
    street = address.street
    city = address.city
    state = address.state
    postal_code = address.postal_code
    country = address.country

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
            address.description = description
            address.suite_or_pobox = suite_or_pobox
            address.building = building
            address.street = street
            address.city = city
            address.state = state
            address.postal_code = postal_code
            address.country = country

            address.save()
            user = request.user
            user_profile = UserProfile.objects.get(associated_user=user)
            user_profile.addresses.add(address)
            return redirect("settings")

    context = {"page_header": page_header, "error": error, "action": action,
               "description": description, "suite_or_pobox": suite_or_pobox, "building": building, 
               "street": street, "city": city, "state": state, "postal_code": postal_code, "country": country}
    return render(request, "auth/address_form.html", context)

@login_required(login_url="login")
def delete_address_view(request, primary_key):

    if request.user.is_superuser:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)
    
    page_header = "Delete Address"
    error = ""
    address = Address.objects.get(id=primary_key)
    
    category = "Address"
    item = f"Address Of Description \"{address.description}\""

    if request.method == "POST":
        address.delete()
        return redirect("settings")

    context = {"page_header": page_header, "error": error, "category": category, "item": item}
    return render(request, "delete.html", context)

@login_required(login_url="login")
def delete_account_view(request):

    if request.user.is_superuser:
        previous_page = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_page)
    
    page_header = "Delete Account"
    error = ""
    user = request.user
    user_profile = UserProfile.objects.get(associated_user=user)

    category = "Account"
    item = f"Your Account With Username \"{user.username}\""

    if request.method == "POST":
        user.delete()
        user_profile.delete()
        return redirect("login")

    context = {"page_header": page_header, "error": error, "category": category, "item": item}
    return render(request, "delete.html", context)

def contact_view(request):
    page_header = "Contact / Feedback"
    error = ""
    user = request.user
    context = {"page_header": page_header, "error": error}
    return render(request, "user_interface/contact.html", context)