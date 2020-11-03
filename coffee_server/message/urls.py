from django.urls import path
from . import views
urlpatterns = [
    path("<int:goods_id>",views.view_messages)
]