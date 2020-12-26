from django.shortcuts import redirect


def logged_in_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            redirect('register')

    return wrapper_func
