"""testdj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.conf.urls import url

from . import view
import myapp.login as login
import myapp.admin as admin
import myapp.identify as identify
import myapp.advertisers as advertisers
import myapp.platforms as platforms
import myapp.recommend as recommend

# 用于前端和后端通信
urlpatterns = [
    url(r'^$', view.hello),
    url(r'show_users$', login.show_users),
    url(r'test$', login.test),
    url(r'check$', login.check),
    url(r'show_labels$', admin.show_labels),
    url(r'add_label$', admin.add_label),
    url(r'update_use$', admin.update_use),
    url(r'show_users$', admin.show_users),
    url(r'cnn$', identify.cnn),
    url(r'get_ads$', advertisers.get_ads),
    url(r'add_ads$', advertisers.add_ads),
    url(r'get_ads_id$', advertisers.get_ads_id),
    url(r'delete_ads$', advertisers.delete_ads),
    url(r'update_pv$', advertisers.update_pv),
    url(r'add_like$', advertisers.add_like),
    url(r'add_cust$', platforms.add_cust),
    url(r'add_words$', platforms.add_words),
    url(r'get_cust$', platforms.get_cust),
    url(r'get_label$', recommend.get_label),
    url(r'get_recommend$', recommend.get_recommend),
    url(r'update_label$', platforms.update_label),
    url(r'upload_cust$', platforms.upload_cust),
]