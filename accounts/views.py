from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token

# Create your views here.
def send_login_email(request):

    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + "?token=" + str(token.uid)
    )
    send_mail(
        'Your login link for Superlists',
        f'Use this link to log in:\n\n{url}',
        'noreply@superlists',
        [email]
    )

    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in." 
    )

    return redirect('/')

def login(request):
    
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    
    return redirect('/')