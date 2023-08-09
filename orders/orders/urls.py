"""orders URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.template.defaulttags import url
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from backend.views import SettingsView, password, logout_request
from backend.views import SettingsView, logout_request, password, main_index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('backend.main_urls', namespace='main_backend')),
    path('api/v1/', include('backend.urls', namespace='backend'))
]

urlpatterns += [
    # ВАШИ URL-АДРЕСА
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('oauth/', include('social_django.urls', namespace='social')),  # <-- here

    path('settings/', SettingsView.as_view(), name='settings'),
    path('settings/password/', password, name='password'),

    path('logout', logout_request, name="logout"),
    path('home', main_index, name="home"),
]
