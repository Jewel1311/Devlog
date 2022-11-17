from django.http import HttpResponseNotFound


#restrict users form admin views
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseNotFound('<h2>You are not authorized to view this page</h2>')
    return wrapper_func