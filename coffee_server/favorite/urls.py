from django.urls import path
from . import views

urlpatterns = [
    path('<str:user_id>',views.FavoriteViews.as_view()),
    path('<str:user_id>/goods_id/<str:delete_id>',views.FavoriteViews.as_view()),
]