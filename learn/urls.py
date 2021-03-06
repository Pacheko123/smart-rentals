"""learn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from login import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index, name = 'home'),
    path('login/',views.log, name = 'log'),
    path('register/',views.register, name = 'register'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('mpesa/',views.mpesa, name = 'mpesa'),
    path('access/token', views.getAccessToken, name='get_mpesa_access_token'),

]
