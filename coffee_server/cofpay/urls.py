from django.urls import path
from . import views
urlpatterns = [
    # http://127.0.0.1:8000/payment/jump/  ftp项目整理
    path("<int:user_id>",views.JumpView.as_view()),
    path('result/',views.ResultView.as_view())
]