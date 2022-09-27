from datetime import datetime
from django.shortcuts import render, redirect
from core.forms import PostForm, UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from . import decorators



def home(request):
    return render(request, 'core/home.html')

@decorators.check_loggedin
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


@decorators.check_loggedin
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            passw = form.cleaned_data['password']
            user = authenticate(request,username = uname, password = passw )
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Invalid credentials')
                return redirect('login_view')
    else:
        form = LoginForm()
    return render(request, 'core/login.html',{'form':form})
    

def write_post(request):
    if request.method == "POST":
        pass
    else:
        form = PostForm()
        return render(request, 'core/write.html',{'form':form})   
