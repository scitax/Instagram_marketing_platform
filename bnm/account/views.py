from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CreateUserForm, Advertisement_posting_form
from .decorators import logged_in_user, logged_in_company, logged_in_blogger
from django.views import View


class Main_page(View):
    @logged_in_user
    def get(self, request):
        postings = Advertisement_posting.objects.all()
        context = {'postings': postings}
        if request.user.usertype == 'Company':
            return render(request, 'advetiser/main_advetiser.html', context)
        if request.user.usertype == 'Blogger':
            return render(request, 'blogger/main_blogger.html', context)


class My_postings(View):
    @logged_in_company
    def get(self, request):
        user_id = request.user.pk
        my_postings_query = Advertisement_posting.objects.filter(advertiser=user_id)
        context = {'my_postings_query': my_postings_query}
        return render(request, 'advetiser/my_postings.html', context)


class RegisterPage(View):
    def get(self, request):
        user_form = CreateUserForm()
        context = {'user_form': user_form}
        return render(request, 'register.html', context)

    def post(self, request):
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('/login/')


class LoginPage(View):
    def get(self, request):
        context = {}
        return render(request, 'login.html', context)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return self.get(request)


class LogoutUser(View):
    def get(self, request):
        logout(request)
        return redirect('/register/')


class New_posting(View):
    @logged_in_company
    def get(self, request):
        platforms_list = Platform.objects.all()
        context = {'platforms_list': platforms_list}
        return render(request, 'advetiser/new_posting.html', context)

    @logged_in_company
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        description = request.POST.get('description')
        platform = request.POST.get('platform')
        platform_obj = Platform.objects.get(platform=platform)
        user = request.user

        post = Advertisement_posting(title=title, description=description)
        post.advertiser = user
        post.platform = platform_obj
        post.save()
        return redirect('/')


class Submit_posting(View):
    @logged_in_blogger
    def get(self, request, *args, **kwargs):
        user = request.user
        pk = kwargs.get('pk')
        advertisement = Advertisement_posting.objects.get(id=pk)
        advertisement.accepted_blogger.add(user)
        advertisement.save
        return redirect('/')


class My_posting(View):
    @logged_in_company
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        advertisement = Advertisement_posting.objects.get(id=pk)
        advetiser_id = request.user.id
        context = {'advertisement': advertisement, 'advetiser_id': advetiser_id}
        return render(request, 'advetiser/my_posting.html', context)


class Start_chat(View):
    @logged_in_user
    def post(self, request):
        user_1_id = request.POST.get('user_1')
        user_2_id = request.POST.get('user_2')
        user_1 = User.objects.get(id=user_1_id)
        user_2 = User.objects.get(id=user_2_id)
        chat = Chat.start(user_1, user_2)
        return redirect(f'/messages/{chat.id}/')


class Chat(View):
    @logged_in_user
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        message = None
        context = {'message': message}
        return redirect('/')


class All_chats(View):
    @logged_in_user
    def get(self, request):
        user = request.user
        chats = Chat.objects.filter(user=user)
        context = {'chats': chats}
        return render(request, 'advetiser/my_posting.html', context)
