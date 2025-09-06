"""
URL configuration for accounts app.
"""

from django.urls import path
# from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts'

# API routes will be added when we create the viewsets
# router = DefaultRouter()

urlpatterns = [
    # Basic placeholder paths for now
    # API routes will be added later
    # path('api/', include(router.urls)),
    
    # Authentication endpoints (will add after installing JWT)
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('wallet/', views.WalletView.as_view(), name='wallet'),
]