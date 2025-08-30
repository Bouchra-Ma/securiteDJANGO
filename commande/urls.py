from django.urls import path, include
from . import views
from rest_framework import routers
from .views_api import ProductViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# DRF Router
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    # Pages classiques avec JWT
    path('', views.home_jwt_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_jwt_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('form/', views.form, name='form'),
    
    path('buy_product/<int:product_id>/', views.buy_product, name='buy_product'),
    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API
    path('api/', include(router.urls)),

    # Anciennes routes basées sur l'authentification par session (commentées)
    
    #path('', views.home, name='home'),
    #path('login/', views.login_view, name='login'),
    #path('products/', views.products, name='products'),
    #path('dashboard/', views.dashboard, name='dashboard'),
     # --- tes APIs JWT ---
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('api/products/', views.api_products, name='api_products'),
]