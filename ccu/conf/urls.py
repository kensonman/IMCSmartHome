"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webconsole import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^cmd/?$', views.cmd, name='cmd'),
	url(r'^login/?$', views.login, name='login'),
	url(r'^logout/?$', views.logout, name='logout'),
	url(r'^appliances/?$', views.appliances, name='appliances'),
	url(r'^appliances/(?P<aid>[^/]+)/?$', views.appliance, name='appliance'),
	url(r'^users/?$', views.users, name='users'),
]
