from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.detect_emotion, name='index'),
]