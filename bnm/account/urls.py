from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='home'),
    path('register/', views.registerPage, name="register"),
    path('login/', views.logignPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('new-posting/', views.new_add_posting, name='new_add'),
    path('my-postings/', views.my_postings, name='my_postings'),

    path('submit-posting/<str:pk>/', views.submit_posting, name='submit_posting'),


]
