from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
 
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    
    path("settings", views.settings_view, name="settings"),
    path("delete_account", views.delete_account_view, name="delete_account"),

    path("add_address", views.add_address_view, name="add_address"),
    path("update_address/<str:primary_key>", views.update_address_view, name="update_address"),
    path("delete_address/<str:primary_key>", views.delete_address_view, name="delete_address"),

    path("contact", views.contact_view, name="contact"),
    path("feedback", views.feedback_view, name="feedback"),

]
