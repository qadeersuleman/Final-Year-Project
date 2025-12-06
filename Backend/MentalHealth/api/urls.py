from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from Chatbot.views import mental_health_chat as chatbot_view
from .views import ArticleListView, ArticleDetailView


urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="login"),
    path('editprofile/',views.edit_profile, name='edit_profile'),
    path('assessments/', views.create_assessment, name='create_assessment'),
    path('audio-analysis/', views.audio_analysis_view, name='audio-analysis'),

    path('csrf-token/', views.get_csrf_token, name='csrf_token'),




    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="article-detail"),

    path('articles/<int:pk>/like/', views.like_article, name='like_article'),
    path('articles/<int:pk>/like-status/', views.check_article_like_status, name='check_like_status'),
    path('articles/<int:pk>/view/', views.track_article_view, name='track_article_view'),



    # Get from chatbot data at here
    path("chats/", chatbot_view, name="mental_health_chat"),

]

# For development, add this to your urls.py:
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)