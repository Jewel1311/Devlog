from django.http import Http404, HttpResponseNotFound
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
            return HttpResponseNotFound('<h2>Page not found</h2>')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
