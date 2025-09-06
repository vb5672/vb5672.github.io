"""
URL configuration for AI ChatBot project.

This configures all the main URL routes for the AI ChatBot application
including API endpoints, admin interface, and frontend routes.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (will be added gradually)
    # path('api/v1/', include('api.urls')),
    
    # Authentication (will be added when JWT is set up)
    # path('auth/', include('accounts.urls')),
    # path('accounts/', include('allauth.urls')),
    
    # App-specific URLs (will be added gradually)
    # path('payments/', include('payments.urls')),
    # path('chat/', include('chat.urls')),
    # path('billing/', include('billing.urls')),
    
    # API Documentation (will be added when drf_spectacular is installed)
    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Frontend (main chat interface)
    path('', TemplateView.as_view(template_name='chat/index.html'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
