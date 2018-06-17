from django.urls import path
from rest_framework import routers

import api.views

api_urls = [
    path('neurovault/<slug:image>/qr', api.views.qr, name='qr'),
    path('neurovault/<slug:image>/models/<slug:hemisphere>', api.views.hemisphere, name='hemisphere'),
]
