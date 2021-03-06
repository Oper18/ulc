# coding: utf-8
"""ulc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from championat.views import ULCBaseTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('accounts.urls'), name='accounts'),
    re_path(r'^', include('championat.urls'), name='championat'),
    re_path(r'^contacts/$', ULCBaseTemplateView.as_view(template_name='contacts.html')),
    re_path(r'^', include('api.v1.urls'), name='api')
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
