"""celery消费者模块"""
from coffee_server.celery import app
# 导入邮箱模块
from django.core.mail import send_mail
from django.conf import settings

@app.task
def send_varcode_email(email_address,varcode):
    subject = "coffee story 验证邮件"
    html_message = """
    <p>尊敬的用户</p>
    <p>您选购的商品已快马加鞭向您赶去，请注意查收</p>
    <p>订单信息：{}</p>
    """.format(varcode)
    # 发送邮件 标题 消息 邮件发送者 html格式信息
    send_mail(subject,'',settings.EMAIL_HOST_USER,[email_address],html_message=html_message)