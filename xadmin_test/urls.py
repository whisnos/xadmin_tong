"""xadmin_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
# from django.contrib import admin
from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter, SimpleRouter
import xadmin
from users.views import UserInfoViewset, NoteInfoViewset, FeedBackInfoViewset
from xadmin_test.settings import STATIC_ROOT

route = SimpleRouter()
route.register(r'user/info', UserInfoViewset, base_name="user/info")
route.register(r'note', NoteInfoViewset, base_name="note")
route.register(r'report', FeedBackInfoViewset, base_name="report")
urlpatterns = [
    url(r'^', include(route.urls)),
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}), # 解决静态文件加载失败问题
]
