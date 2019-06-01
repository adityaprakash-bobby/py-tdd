from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from .models import Item, List
from .forms import ItemForm

# Create your views here.
def home_page(request):
 
    return render(request, 'home.html', {
        'form': ItemForm(),
    })


def views_list(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':

        try:

            item = Item(text=request.POST['item_text'], list=list_ob)
            item.full_clean()
            item.save()
            return redirect(list_ob)    

        except ValidationError as e:
            
            error = "You can't have an empty list item"
            
    return render(request, 'list.html', {
        'list' : list_ob,
        'error' : error
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
    
    return redirect(list_ob)

def add_item(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_ob)
    return redirect(list_ob)