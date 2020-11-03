from django.urls import path
from . import views

urlpatterns = [
    path('<str:goods_id>',views.GoodsView.as_view()),

]