# -*- coding: utf-8 -*-
"""
# @项目名称 :shovel_complement
# @文件名称 :alert.py
# @作者名称 :sxzhang1
# @日期时间 :2024/2/23 14:01
# @文件介绍 :
"""
import base64
import hashlib
import hmac
import time
from urllib.parse import quote_plus

import requests


class DingRobot:
    def __init__(self):
        self.secret = "SEC999d3ff220cea418c54ab02c181b9db122f76e1db349f69e45cc507d9ca64ad0"
        self.url = "https://oapi.dingtalk.com/robot/send"
        self.headers = {
            "Content-Type": "application/json"
        }

    @staticmethod
    def sign_secret(secret, timestamp):
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = quote_plus(base64.b64encode(hmac_code))
        return sign

    def get_params(self):
        timestamp = str(round(time.time() * 1000))
        params = {
            "access_token": "49eec26b2a4532e64e47e7d90376c3b305c10328980bb3572d91e7587bb87cbd",
            "timestamp": timestamp,
            "sign": self.sign_secret(self.secret, timestamp)
        }
        return params

    def send_request(self, msg):
        message = {"msgtype": "text", "text": {"content": msg}}
        response = requests.request(method="POST", url=self.url, headers=self.headers, json=message,
                                    params=self.get_params())
        print(response.json())


