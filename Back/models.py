from django.db import models

from PubFunc.base_db import BaseDB


# Create your models here.

class BackPageUrl(BaseDB):
    page_name = models.CharField(max_length=10, unique=True, null=False, verbose_name="页面名称")
    page_url = models.CharField(max_length=255, null=False, verbose_name="页面链接")
    page_level = models.IntegerField(default=0, verbose_name="页面级别")
    parent_id = models.BigIntegerField(default=0, verbose_name="父级ID")

    class Meta:
        db_table = "back_page_url"
        verbose_name = "后台管理页面路由"
        verbose_name_plural = verbose_name
        ordering = ["ID"]
