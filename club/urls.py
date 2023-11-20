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

    path("add_match", views.add_match_view, name="add_match"),
    path("update_match/<str:primary_key>", views.update_match_view, name="update_match"),
    path("delete_match/<str:primary_key>", views.delete_match_view, name="delete_match"),

    path("add_player", views.add_player_view, name="add_player"),
    path("update_player/<str:primary_key>", views.update_player_view, name="update_player"),
    path("delete_player/<str:primary_key>", views.delete_player_view, name="delete_player"),

    path("add_merch", views.add_merch_view, name="add_merch"),
    path("update_merch/<str:primary_key>", views.update_merch_view, name="update_merch"),
    path("delete_merch/<str:primary_key>", views.delete_merch_view, name="delete_merch"),

    path("contact", views.contact_view, name="contact"),
    path("feedback", views.feedback_view, name="feedback"),

    path("soccer_info", views.soccer_info_view, name="soccer_info"),

]
