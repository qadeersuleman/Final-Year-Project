from django.urls import path
from . import views

urlpatterns = [
    path("chats/", views.mental_health_chat, name="mental_health_chat"),
]
