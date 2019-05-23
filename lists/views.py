from django.shortcuts import render, redirect, HttpResponse
from .models import Item, List

# Create your views here.
def home_page(request):

    return render(request, 'home.html')


def views_list(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_ob)
    return render(request, 'list.html', {
        'list' : list_ob
    })

def new_list(request):

    list_ob = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_ob)
    return redirect(f'/lists/{list_ob.id}/')

def add_item(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_ob)
    return redirect(f'/lists/{list_ob.id}/')