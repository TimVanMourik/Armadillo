"""giraffe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin

import armadillo.views

app_name = 'app'

urlpatterns = [
    url(r'^$',                          armadillo.views.index, name='index'),
    path('neurovault/<slug:image>/',    armadillo.views.image, name='vault-image'),
    path('neurovault/<slug:image>/qr',  armadillo.models.qr, name='qr'),
    path('neurovault/<slug:image>/models/<slug:hemisphere>',  armadillo.models.hemisphere, name='hemisphere'),
    path('neurovault/<slug:image>/gifti/<slug:hemisphere>',  armadillo.models.gifti, name='gifti'),
    # path('neurovault/<slug:image>/lh',  armadillo.models.lh, name='lh'),
    # path('neurovault/<slug:image>/lh_gifti',  armadillo.models.lh_gifti, name='lh_gifti'),
    # path('neurovault/<slug:image>/rh',  armadillo.models.rh, name='rh'),
    # path('neurovault/<slug:image>/rh_gifti',  armadillo.models.rh_gifti, name='rh_gifti'),
    # path('test/<slug:image>/',          armadillo.views.test,  name='test'),
    url(r'^admin/?',                    admin.site.urls),
]
