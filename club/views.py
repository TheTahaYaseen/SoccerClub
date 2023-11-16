from django.shortcuts import render

# Create your views here.
def home_view(request):
    page_header = "Home"
    context = {"page_header": page_header}
    return render(request, "user_interface/home.html", context)