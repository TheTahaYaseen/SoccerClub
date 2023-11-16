from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import phonenumbers

from django.contrib.auth.models import User
from ..models import UserProfile

def email_validation(email):    
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def phone_number_validation(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "PK")
        is_valid = phonenumbers.is_valid_number(parsed_number)
        return is_valid
    except phonenumbers.NumberParseException:
        return False

def username_already_used(username):
    if User.objects.filter(username=username).exists():
        return True
    else:
        return False

def email_already_used(email):
    if UserProfile.objects.filter(email=email).exists():
        return True
    else:
        return False

def validate_credentials(username, email, phone_number, password, password_confirmation):
    error = ""
    if not username:
        error = "Username Cannot Be Empty!"
    elif not email:
        error = "Email Cannot Be Empty!"
    elif not phone_number:
        error = "Phone Number Cannot Be Empty!"
    elif not password:
        error = "Password Cannot Be Empty!"
    elif not password_confirmation:
        error = "Password Confirmation Cannot Be Empty!"
    elif password != password_confirmation:
        error = "Password And Password Confirmation Must Be Same!"
    elif not email_validation(email):
        error = "Please Use A Valid Email!"
    elif not phone_number_validation(phone_number):
        error = "Please Use A Valid Phone Number!"
    elif username_already_used(username):
        error = "Username Already Used!"
    elif email_already_used(email):
        error = "Email Already Used!"

    return error

def create_user_profile(username, email, phone_number, password):
    error = ""
    try:
        associated_user, created = User.objects.get_or_create(
            username = username,
        )
        UserProfile.objects.create(
            associated_user = associated_user,
            email = email,
            phone_number = phone_number
        )
    except Exception:
        error = "An Error Occured While Registering You!"
    return error