import json

import requests

from xadmin_test.settings import APPID, SECRET


def make_openid(JSCODE):
    r = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session?appid=' + APPID + '&secret=' + SECRET + '&js_code=' + JSCODE + '&grant_type=authorization_code')
    result = r.content
    dict_result=json.loads(result)
    return dict_result