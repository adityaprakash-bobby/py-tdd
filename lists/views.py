from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List

# Create your views here.
def home_page(request):

    return render(request, 'home.html')


def views_list(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_ob)
        return redirect(f'/lists/{list_id}/')    
    items = Item.objects.filter(list=list_ob)

    return render(request, 'list.html', {
        'list' : list_ob
    })

def new_list(request):

    list_ob = List.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], list=list_ob)
    
    try:

        item.full_clean()
        item.save()
    
    except ValidationError as e:

        list_ob.delete()
        error = "You can't have an empty list item"
        
        return render(request, 'home.html', {
            'error': error
        })
    
    return redirect(f'/lists/{list_ob.id}/')

def add_item(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_ob)
    return redirect(f'/lists/{list_ob.id}/')