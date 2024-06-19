# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :serializers.py
# @作者名称 :sxzhang1
# @日期时间 :2024/4/30 14:14
# @文件介绍 :
"""
from rest_framework import serializers

from .models import AppList


class AppListSerializer(serializers.Serializer):
    # ID = serializers.IntegerField(read_only=True)
    # crt_time = serializers.DateTimeField(read_only=True)
    # upd_time = serializers.DateTimeField(read_only=True)
    # is_del = serializers.BooleanField(default=True, read_only=True)

    app_name = serializers.CharField(max_length=10, label="应用名称")
    app_img = serializers.CharField(max_length=255, label="应用图片")
    app_url = serializers.CharField(max_length=255, label="应用链接")
    app_desc = serializers.CharField(label="应用介绍")

    user_id = serializers.IntegerField(label="用户信息")
    app_group_id = serializers.IntegerField(label="分组ID")

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
        model = AppList
