from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('', views.main),
    path('login', views.login_view),
    path('registry', views.registry_view),
    path('logout', views.logout_view),
    path('file_manager', views.file_manager_view),
    path('documents/', views.document_list),
    path('upload/', views.upload_document),
    path('delete/<int:document_id>/', views.delete_document),
]