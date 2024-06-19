from django.db import models

from PubFunc.base_db import BaseDB


# Create your models here.
class AppGroup(BaseDB):
    group_name = models.CharField(max_length=10, unique=True, null=False, verbose_name="分组名称")
    group_level = models.IntegerField(default=0, verbose_name="分组等级")

    class Meta:
        db_table = "app_group"
        verbose_name = "应用分组"
        verbose_name_plural = verbose_name
        ordering = ["ID"]


class AppList(BaseDB):
    app_name = models.CharField(max_length=10, verbose_name="应用名称")
    app_img = models.CharField(max_length=255, null=True, default="", verbose_name="应用图片")
    app_url = models.CharField(max_length=255, verbose_name="应用链接")
    app_desc = models.TextField(null=True, verbose_name="应用介绍")

    user_id = models.BigIntegerField(null=False, verbose_name="用户信息")
    app_group_id = models.BigIntegerField(verbose_name="分组ID")

    class Meta:
        db_table = "app_list"
        verbose_name = "应用信息"
        verbose_name_plural = verbose_name
        ordering = ["ID"]
