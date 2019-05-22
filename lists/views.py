from django.shortcuts import render, redirect, HttpResponse
from .models import Item, List

# Create your views here.
def home_page(request):

    return render(request, 'home.html')


def views_list(request):
    
    items = Item.objects.all()
    return render(request, 'list.html', {
        'items' : items,
    })

def new_list(request):

    list_ob = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_ob)
    return redirect('/lists/the-only-list-in-the-world/')