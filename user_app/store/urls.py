from django.urls import path

from . import views
from django.views.decorators.cache import cache_page

app_name = 'store'


urlpatterns = [
    path('', views.homepage_request, name='index'),
]