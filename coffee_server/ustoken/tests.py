# from django.test import TestCase
# import jwt
# import time
# # Create your tests here.
# keysss = '123456'
# user_id = 1
# now = time.time()
# expire = 300
# payload = {"user_id": user_id, "exp": now + expire}
# token = jwt.encode(payload, keysss, algorithm="HS256")
#
#
# playload = jwt.decode(token,keysss)
# print(playload)
from urllib import parse

print(parse.unquote('%E5%92%96%E5%95%A1%E5%95%8A'))
# print()
