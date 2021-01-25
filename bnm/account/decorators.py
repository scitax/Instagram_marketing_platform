from django.shortcuts import redirect


def logged_in_user(view_func):
    """
    Checking if user is registered
    :param view_func:
    :return: view_func: or redirect register login page
    """
    def wrapper_func(request, *args, **kwargs):
        if request.request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrapper_func


def logged_in_company(view_func):
    """
    Checking if user is registered and is company
    :param view_func:
    :return: view_func: or redirect register login page
    """
    def wrapper_func(request, *args, **kwargs):
        if request.request.user.is_authenticated and request.request.user.usertype == 'Company':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('register')

    return wrapper_func


def logged_in_blogger(view_func):
    """
    Checking if user is registered and is blogger
    :param view_func:
    :return: view_func: or redirect register login page
    """
    def wrapper_func(request, *args, **kwargs):
        if request.request.user.is_authenticated and request.request.user.usertype == 'Blogger':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('register')

    return wrapper_func
