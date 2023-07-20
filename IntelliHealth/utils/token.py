import time
import hashlib

from django.core import signing
from django.conf import settings


HEADER = {'typ': 'JWT', 'alg': 'HS256'}
KEY = settings.SECRETS['SIGNING']['KEY']
SALT = settings.SECRETS['SIGNING']['SALT']


# 加密
def encrypt(obj):
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


# 解密
def decrypt(src):
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


# 生成token信息
def create_token(user_id):
    exp_time = 60 * 60 * 24
    # 1.加密头信息
    header = encrypt(HEADER)
    # 2.构造Payload(有效期1天)
    payload = {"user_id": user_id, "iat": time.time(), "exp": time.time() + exp_time}
    payload = encrypt(payload)
    # 3.生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    return token


def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload


def get_id(token):
    return get_payload(token)['user_id']


def get_exp_time(token):
    payload = get_payload(token)
    return payload['exp']


def check_token(token):
    return get_exp_time(token) > time.time()
