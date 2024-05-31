from django.db import models

from PubFunc.base_db import BaseDB


# Create your models here.
class User(BaseDB):
    account = models.CharField(max_length=255, unique=True, null=False, verbose_name="账户名称")
    password = models.CharField(max_length=255, null=False, verbose_name="账户密码")
    nickname = models.CharField(max_length=255, default="匿名", verbose_name="账户昵称")
    email = models.CharField(max_length=255, verbose_name="个人邮箱")
    sex = models.BooleanField(default=True, verbose_name="个人性别")
    birthday = models.DateField(verbose_name="出生日期")

    class Meta:
        db_table = "user_info"
        verbose_name = "账户信息"
        verbose_name_plural = verbose_name
        ordering = ["ID"]
