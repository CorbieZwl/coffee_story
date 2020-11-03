from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_id>',views.CartViews.as_view()),
    path('<str:user_id>/goods_id/<str:delete_id>',views.CartViews.as_view()),
    path('<str:user_id>/<str:cart_goods_id>/<str:num>',views.CartViews.as_view()),
]