from django.urls import path

from . import views
from django.views.decorators.cache import cache_page

app_name = 'main'


urlpatterns = [
    path('', views.homepage_request, name='homepage'),
    path("signup/", views.signup_request, name="signup"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]