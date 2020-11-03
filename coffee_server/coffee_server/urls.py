"""coffee_server URL Configuration

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
from django.urls import path, include
from goods import views as goods_views
from user import views as user_views
from ustoken import views as ustoken
from favorite import views as favorite_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 试用 数据插入
    path("addgoodsdata", goods_views.asdas),
    # 获取数据
    path("v1/goods", goods_views.GoodsView.as_view()),
    # v1/goods/${o.id}
    path("v1/goods/", include("goods.urls")),
    # 插入用户数据  unique是由django完成的
    path("adduserinfo", user_views.adduserinfo),
    path("v1/messages/", include("message.urls")),
    # user应用下的试图模块的视图函数
    path("v1/user", user_views.UserView.as_view()),
    # 获取一个用户的属性
    path('v1/user/', include('user.urls')),
    # 返回一个token
    path("v1/ustoken", ustoken.UstokenView.as_view()),
    path('v1/favorite/', include('favorite.urls')),
    # 订单模块
    path('v1/indent/',include('indent.urls')),
    # 购物车模块
    path('v1/cart/',include('cart.urls')),
    path('cofpay/',include('cofpay.urls')),
]
