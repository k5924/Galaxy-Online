"""GalaxyOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# imports admin to use for urls
from django.urls import include, path
# imports include and path to use for mapping urls
from django.conf import settings
# imports settings from settings.py
from django.conf.urls.static import static
# imports static to store/load static files from html forms

urlpatterns = [
    path('', include('Home.urls')),
    path('admin/', admin.site.urls),
    # this allows my apps urls and the admin urls to be used
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# added static line from django docs and allows images to be stored in MEDIA_ROOT
