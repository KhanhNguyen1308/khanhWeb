from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', views.main),
    path('login', views.login_view),
    path('file_manager', views.file_manager_view),
]