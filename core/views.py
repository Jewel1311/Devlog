from datetime import datetime
from django.shortcuts import render, redirect
from core.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django import forms


def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(False)
            user.date_joined = datetime.now()
            user.save()
            return redirect('home')
    else:
        form = UserRegistrationForm
    return render(request, 'core/register.html', {'form':form})
    
