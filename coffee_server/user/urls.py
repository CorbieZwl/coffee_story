from django.urls import path
from . import views
urlpatterns = [
    # 获取验证码
    path('varcode',views.create_verification_code),
    path('<str:user_id>',views.UserView.as_view()),

]