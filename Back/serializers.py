# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :serializers.py
# @作者名称 :sxzhang1
# @日期时间 :2024/4/30 14:14
# @文件介绍 :
"""
from rest_framework import serializers

from .models import BackPageUrl, Status


class BackPageUrlSerializer(serializers.Serializer):
    ID = serializers.IntegerField(read_only=True)
    crt_time = serializers.DateTimeField(read_only=True)
    upd_time = serializers.DateTimeField(read_only=True)
    is_del = serializers.BooleanField(default=True, read_only=True)

    page_name = serializers.CharField(max_length=10, label="页面名称")
    page_url = serializers.CharField(max_length=255, label="页面链接")
    page_level = serializers.IntegerField(label="页面级别")
    parent_id = serializers.IntegerField(label="父级ID")

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
        model = BackPageUrl


class StatusSerializer(serializers.Serializer):
    # ID = serializers.IntegerField(read_only=True)
    # crt_time = serializers.DateTimeField(read_only=True)
    # upd_time = serializers.DateTimeField(read_only=True)
    # is_del = serializers.BooleanField(read_only=True)

    statu_code = serializers.IntegerField(label="状态码")
    inter_en = serializers.CharField(max_length=255, label="英文信息")
    inter_ch = serializers.CharField(max_length=255, label="中文信息")
    explain = serializers.CharField(max_length=255, label="解释信息")
    inter_solu = serializers.CharField(max_length=255, label="搞怪信息")

    def create(self, validated_data):
        ...

    def update(self, instance, validated_data): ...

    def delete(self): ...

    class Meta:
        model = Status
