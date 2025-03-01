"""zinc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
# from django.contrib import admin

from ccs import views
from ccs.site_config import nav_config
from ccs.site_views import site_obj
# from ccs.views import news_list
site_obj.config_nav(nav_config)
urlpatterns = [
    path('', include(site_obj.urls)),
    path('LDA/', views.LDA.as_view()),
    path('news_list/', views.news_list, name='news_list'),
    path('run_scripts/', views.run_scripts, name='run_scripts'),
    path('news/<int:news_id>/', views.news_detail, name='news_detail')
    # path('admin/', admin.site.urls)
]

