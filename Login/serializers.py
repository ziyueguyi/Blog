# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :serializers.py
# @作者名称 :sxzhang1
# @日期时间 :2024/4/30 14:14
# @文件介绍 :
"""
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.Serializer):
    ID = serializers.IntegerField(read_only=True)
    crt_time = serializers.DateTimeField(read_only=True)
    upd_time = serializers.DateTimeField(read_only=True)
    is_del = serializers.BooleanField(default=True, read_only=True)

    account = serializers.CharField(max_length=255,  label="账户名称")
    password = serializers.CharField(max_length=255,  label="账户密码")
    nickname = serializers.CharField(max_length=255,  label="账户昵称")
    email = serializers.CharField(max_length=255, label="个人邮箱")
    sex = serializers.BooleanField(label="个人性别")
    birthday = serializers.DateField(label="个人生日")

    # def create(self, validated_data):
    #     account = validated_data.get("account")
    #     if not User.objects.filter(account=account).count():
    #         return User.objects.create(**validated_data)
    #     else:
    #         return False

    #
    # def update(self, instance, validated_data): ...
    #
    # def delete(self): ...

    class Meta:
        model = User
