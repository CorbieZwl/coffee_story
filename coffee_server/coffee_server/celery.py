from celery import Celery
from django.conf import settings
import os

# 为celery配置环境变量  让celery知道settings.py文件的位置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_server.settings')

# 创建应用
app = Celery('coffee_server')
# 配置应用
app.conf.update(
    # 配置broker
    BROKER_URL='redis://:@127.0.0.1:6379/1',
)
# 告诉celery生产者函数位置
app.autodiscover_tasks(settings.INSTALLED_APPS)
