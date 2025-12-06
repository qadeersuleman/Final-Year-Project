from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('emotion/', include('EmotionDetection.urls')),
    path('', include('Extra.urls')),
    path('', include('Chatbot.urls')),
    path('api/', include('AppointDoctor.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)