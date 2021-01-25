from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main_page.as_view(), name='home'),
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('login/', views.LoginPage.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),
    path('new-posting/', views.New_posting.as_view(), name='new-posting'),
    path('my-postings/', views.My_postings.as_view(), name='my-postings'),
    path('submit-posting/<str:pk>/', views.Submit_posting.as_view(), name='submit-posting'),
    path('my-posting/<str:pk>', views.My_posting.as_view(), name='my-posting'),
    path('messages/<str:pk>', views.Chat.as_view(), name='messages'),
    path('chats/', views.All_chats.as_view, name='all-chats'),
    path('start-chat/', views.Start_chat.as_view, name='start-chats')
]
