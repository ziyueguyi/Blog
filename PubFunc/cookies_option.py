# -*- coding: utf-8 -*-
"""
# @项目名称 :Blog
# @文件名称 :cookies_option.py
# @作者名称 :sxzhang1
# @日期时间 :2024/6/3 11:37
# @文件介绍 :
"""
from django.http import HttpResponse


def set_cookie(response):
    response.set_cookie('cookie_name', 'cookie_value', max_age=3600)  # 设置cookie，有效期为1小时
    return response


def get_cookie(request):
    cookie_value = request.COOKIES.get('cookie_name')  # 读取cookie
    return HttpResponse(f'The value of the cookie is: {cookie_value}')


def delete_cookie(response):
    response.delete_cookie('cookie_name')  # 删除cookie
    return response
