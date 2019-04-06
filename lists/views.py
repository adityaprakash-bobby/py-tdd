from django.shortcuts import render, HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse(b'<h1>Home Page for site</h1>')