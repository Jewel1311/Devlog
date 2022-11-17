from django.http import HttpResponseNotFound
from django.shortcuts import redirect

def check_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#restrict super user from loggin into feeds
def restrict_superuser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseNotFound('<h2>You are not authorized to view this page</h2>')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#redirect admin to admin page if admin is logged in
def redirect_adminhome(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

