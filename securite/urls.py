"""
URL configuration for securite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
# You can register your viewsets here, e.g.:
# router.register(r'your_endpoint', YourViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', include('commande.urls')), 
    path('api/', include(router.urls)),

    # Ancienne route utilisant l'authentification par session (commentée)
    
    #path('', home, name='home'),
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

