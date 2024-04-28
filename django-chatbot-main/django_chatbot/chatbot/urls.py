from django.urls import path
from . import views

urlpatterns = [
    path('chatbot', views.chatbot, name='chatbot'),
    path('login', views.login, name='login'),
    path('', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    
]