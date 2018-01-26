"""first_project URL Configuration

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
from django.contrib import admin
from django.urls import path
from first_app import views
#from django.contrib.auth.views import login
#from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView


urlpatterns = [
    path(r'', TemplateView.as_view(template_name='home.html'), name='home'),
    path(r'login', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path(r'logout', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    path(r'dashboard/testcase', views.testcase_run, name="testcase_run"),
    #path(r'testcase', views.testcase_run, name="testcase_run"),
    #path(r'accounts/profile/', views.login, name="login1"),
    # path(r'lan', views.lan, name="lan"),
    # path(r'lan', views.lan, name="wan"),
    # path(r'lan', views.lan, name="wlan"),
    # path(r'lan', views.lan, name="system"),

    path(r'dashboard/', views.dashboard, name="dashboard"),
    #path('', views.index, name="index"),
    #path('login', views.login, name="login"),

 #   path(r'^login/$', auth_views.login, name='login'),
  #  path(r'^logout/$', auth_views.logout, name='logout'),
    path('admin/', admin.site.urls),
]