import jwt
from django.conf import settings
import time
from user.models import UserInfo
from django.http import JsonResponse

def make_token(user_id, expire=3600 * 24):
    key = settings.JWT_TOKEN_KEY
    now = time.time()
    payload = {"user_id": user_id, "exp": now + expire}
    return jwt.encode(payload, key, algorithm="HS256")


# 获取toklen检查token是否过期 过期则返回空 不过期则返回用户id
def getuser_token(request):
    token = request.META.get("HTTP_AUTHORIZATION")
    if not token:
        return None
    try:
        payload = jwt.decode(token.encode(), settings.JWT_TOKEN_KEY)
    except Exception as e:
        return None
    else:
        return payload['user_id']


# 检测登陆状态的装饰器
def login_check(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        # 判断token是否为空
        if token == 'null':
            result = {"code": 60001, "error": "请先登陆"}
            return JsonResponse(result)
        try:
            # 判断token是否有效 过期 或被篡改
            payload = jwt.decode(token.encode(), settings.JWT_TOKEN_KEY)
            # print(payload)
        except Exception as e:
            print(e)
            result = {"code": 60001, "error": "请先登陆"}
            return JsonResponse(result)
        else:
            user_id = payload['user_id']
            # 用户必然存在 异常捕获 以免扣钱
            try:
                user = UserInfo.objects.get(id=user_id)
            except Exception as e:
                result = {"code": 60001, "error": "token is error"}
                return JsonResponse(result)
            else:
                # 将用户对象传入request 便于后续使用
                request.myuser = user
        return func(request, *args, **kwargs)

    return wrapper
