from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Item, List
from .forms import ItemForm, ExistingListItemForm
User = get_user_model()

# Create your views here.
def home_page(request):
 
    return render(request, 'home.html', {
        'form': ItemForm(),
    })


def views_list(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_ob)

    if request.method == 'POST':

        form = ExistingListItemForm(for_list=list_ob, data=request.POST)
        
        if form.is_valid():
            
            form.save()
            return redirect(list_ob)

    return render(request, 'list.html', {
        'list' : list_ob,
        'form' : form,
    })

def new_list(request):

    form = ItemForm(data=request.POST)

    if form.is_valid():
        
        list_ob = List()
        list_ob.owner = request.user
        list_ob.save()
        form.save(for_list=list_ob)

        return redirect(list_ob)
    
    return render(request, 'home.html', {
        'form': form,
    })

def add_item(request, list_id):
    
    list_ob = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['text'], list=list_ob)
    return redirect(list_ob)

def my_lists(request, email):

    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner':owner})