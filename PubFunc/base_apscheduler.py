# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :base_apscheduler.py
# @作者名称 :sxzhang1
# @日期时间 :2024/5/6 13:37
# @文件介绍 :
"""
import requests
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django_apscheduler.jobstores import DjangoJobStore
from logger.logger import Logger
from rookiepy import rookiepy


class BaseSche(object):
    _instance = None

    # 单例
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = True
        return cls._instance

    def __init__(self):
        if self.__initialized:
            self.__initialized = False
            self._init_()

    def _init_(self):
        self.logger = Logger()
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://elihu-miner.leqee.com",
            "referer": "https://elihu-miner.leqee.com/frontend/index.html",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
        }
        self.new_cookies = dict()
        self.get_cookies()
        self.session = requests.Session()
        self.session.auth = ()
        self.session.cookies.update(self.new_cookies)
        self.session.headers.update(self.headers)
        self.scheduler = self._scheduler()

    def get_cookies(self, domain="leqee.com"):
        """
        获取浏览器cookies
        :param domain:域名,可以通过google的cookies查看
        :return:
        """
        cookies = rookiepy.chrome([domain])
        if cookies:
            for cookie in cookies:
                self.new_cookies.update({cookie["name"]: cookie["value"]})
            self.logger.info("cookies 获取成功")
        else:
            self.logger.exception("cookies 获取失败")

    @staticmethod
    def _scheduler():
        """
        创建定时队列并多线程运行
        :return:
        """
        executors = {
            'default': ThreadPoolExecutor(settings.THREAD_NUM)  # 最多20个线程同时执行
        }
        scheduler = BackgroundScheduler(executors=executors)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        return scheduler

    def add_scheduler_job(self, func, params, sche_id, hour, minute, prompt=True):
        """
        :param params:
        :param func:执行函数
        :param sche_id:定时id
        :param hour:时
        :param minute:分
        :param prompt:是否提示
        :return:
        """
        self.scheduler.add_job(func=func, args=params, trigger="cron", hour=hour, minute=minute, id=sche_id,
                               replace_existing=True,
                               misfire_grace_time=1000 * 90)
        if prompt:
            self.logger.info(
                "执行[{0}]定时任务启动：{1}时{2}分".format(self.scheduler.get_job(sche_id).id, hour, minute))
