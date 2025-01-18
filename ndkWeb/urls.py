"""
URL configuration for ndkWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from home.views import file_manager_view, login_view, logout_view, registry_view, main
from home.views import document_list, delete_document, upload_document
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = "NDK"
admin.site.site_header = "NDK administration"
admin.site.index_title = "administration"
urlpatterns = [
    path("", main, name="home"),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('registry/', registry_view, name="registry"),
    # path('login/',auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('admin/filer/', include('filer.urls')),
    path('file_manager/', file_manager_view, name='file_manager'), 
    # path('accounts/', include('django.contrib.auth.urls')),
    path('documents/', document_list, name='document_list'),
    path('upload/', upload_document, name='upload_document'),
    path('delete/<int:document_id>/', delete_document, name='delete_document'),
]
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)