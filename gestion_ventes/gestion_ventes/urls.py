"""gestion_ventes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import re

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ventes.urls')),
]

# Static files are not served by Django when DEBUG = False
# For ease of development, we still allow Django to serve them
# On the production server, Django won't actually serve the files
# because the web server will handle /static
if settings.DEBUG is False:
    urlpatterns += [
        # Inspiration: https://stackoverflow.com/questions/6405173/static-files-wont-load-when-out-of-debug-in-django#
        url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')), serve, kwargs={'document_root': settings.STATIC_ROOT}),
    ]
