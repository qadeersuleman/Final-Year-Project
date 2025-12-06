from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/health/', views.health_check, name='health_check'),
]