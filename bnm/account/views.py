from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, Add_posting_form
from .decorators import logged_in_user


@logged_in_user
def main_page(request):
    if request.user.usertype == 'Company':
        postings = Add_posting.objects.all()
        context = {'postings': postings}
        return render(request, 'advetiser/main_advetiser.html', context)
    if request.user.usertype == 'Blogger':
        postings = Add_posting.objects.all()
        context = {'postings': postings}
        return render(request, 'blogger/main_blogger.html', context)


@logged_in_user
def my_postings(request):
    if request.user.usertype == 'Company':
        user_id = request.user.pk
        my_postings_query = Add_posting.objects.filter(advertiser=user_id)
        context = {'my_postings_query': my_postings_query}
        return render(request, 'advetiser/my_postings.html', context)
    else:
        return redirect('register')


def registerPage(request):
    user_form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
    context = {'user_form': user_form}
    return render(request, 'register.html', context)


def logignPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@logged_in_user
def new_add_posting(request):
    if request.user.usertype == 'Company':
        add_form = Add_posting_form()
        if request.method == 'POST':
            add_form = Add_posting_form(request.POST)
            if add_form.is_valid():
                add_form.save()
                return redirect('/')
        context = {'add_form': add_form}
        return render(request, 'advetiser/new_posting.html', context)
    else:
        return redirect('register')


@logged_in_user
def submit_posting(request, pk):
    if request.user.usertype == 'Blogger':
        user = request.user
        if request.method == 'POST':
            add_new_blogger = Add_blogger_accepted(add_posting=pk)
            add_new_blogger.accepted_blogger.add(user)
            add_new_blogger.save()
            return redirect('/')
    else:
        return redirect('register')
