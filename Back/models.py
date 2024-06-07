from django.db import models

from PubFunc.base_db import BaseDB


# Create your models here.

class BackPageUrl(BaseDB):
    page_name = models.CharField(max_length=5, unique=True, null=False, verbose_name="页面名称")
    page_url = models.CharField(max_length=255, null=False, verbose_name="页面链接")
    page_level = models.IntegerField(default=0, verbose_name="页面级别")
    parent_id = models.BigIntegerField(default=0, verbose_name="父级ID")

    class Meta:
        db_table = "back_page_url"
        verbose_name = "后台管理页面路由"
        verbose_name_plural = verbose_name
        ordering = ["ID"]


class Status(BaseDB):
    statu_code = models.BigIntegerField(unique=True, null=False, verbose_name="状态码")
    inter_en = models.CharField(max_length=255, verbose_name="英文信息")
    inter_ch = models.CharField(max_length=255, verbose_name="中文信息")
    explain = models.CharField(max_length=255, verbose_name="解释信息")
    inter_solu = models.CharField(max_length=255, verbose_name="搞怪信息")

    class Meta:
        db_table = "status"
        verbose_name = "状态码信息"
        verbose_name_plural = verbose_name
        ordering = ["ID"]
