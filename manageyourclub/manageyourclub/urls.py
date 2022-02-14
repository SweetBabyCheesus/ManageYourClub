"""manageyourclub URL Configuration

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
# Code genutzt: https://www.ordinarycoders.com/blog/article/add-a-custom-favicon-to-your-django-web-app
# favicon.ico von https://pixabay.com/vectors/flag-icon-flag-icon-destination-1636453/ 

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import home_view
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('teams/', include('teams.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('clubs/', include('clubs.urls')),
    path('users/', include('users.urls')),
    path('', home_view, name='home'),
    path('<int:club>/', home_view, name='home'),
    path('members/', include('members.urls')),
    path('notifications/', include('notifications.urls')),
    path('form_builder_example/', include('django_form_builder.urls')),
    path('<int:club>/mebershiprequest/', include('membership_request.urls')),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_URL)