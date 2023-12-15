from django.conf import settings
import hashlib


def md5(date_string):
    # 加盐
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(date_string.encode('utf-8'))
    return obj.hexdigest()
