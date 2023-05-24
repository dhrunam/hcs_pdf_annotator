from rest_framework import urls
from django.urls    import path, include
from . import views


urlpatterns = [
    path('',include(views)),

]
