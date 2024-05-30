# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :base_db.py
# @作者名称 :sxzhang1
# @日期时间 :2024/4/30 13:17
# @文件介绍 :
"""
from django.db import models


class DateTimeFieldFormat(models.DateTimeField):
    """
    数据库datetime类型字段格式化(%Y-%m-%d %H:%M:%S)
    precision:需要保留的小数位数
    """

    def __init__(self, verbose_name=None, name=None, precision=0, **kwargs):
        self.precision = precision
        super().__init__(verbose_name, name, **kwargs)

    def db_type(self, connection):
        return 'datetime(%d)' % self.precision


class BaseDB(models.Model):
    ID = models.BigAutoField(primary_key=True, verbose_name="ID")
    crt_time = DateTimeFieldFormat(auto_now_add=True, verbose_name="创建时间")
    upd_time = DateTimeFieldFormat(auto_now=True, verbose_name="更新时间")
    is_del = models.BooleanField(default=True, verbose_name="是否有效")

    class Meta:
        abstract = True
