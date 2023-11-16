from django.shortcuts import render

# Create your views here.
def home_view(request):
    context = {}
    return render(request, "user_interface/home.html", context)