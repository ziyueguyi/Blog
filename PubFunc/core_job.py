# # -*- coding: utf-8 -*-
# """
# # @项目名称 :LargeMarket
# # @文件名称 :core_job.py
# # @作者名称 :sxzhang1
# # @日期时间 :2024/5/6 10:37
# # @文件介绍 :
# """
# import datetime
# import json
# import math
# import random
# import re
# import time
#
# from apscheduler.schedulers.background import BackgroundScheduler
#
# from Queue.models import Queue, QueueLog
# from Schedules.models import Schedule, SchedulePage, ResponsibleSchedule
# from files.scripts.alert import DingRobot
# from files.scripts.base_apscheduler import BaseSche
#
#
# class CoreJob(BackgroundScheduler):
#     def __init__(self, **options):
#         super().__init__(**options)
#         self.bs = BaseSche()
#
#     def get_queue(self, schedule_id):
#         """
#         根据schedule_id获取前十的运行队列
#         :param schedule_id:
#         :return:
#         """
#         url = "https://elihu-miner.leqee.com/api/QueueController/listTasksInQueue"
#         json_data = {
#             "schedule_id": schedule_id,
#             "page": 1,
#             "page_size": 10,
#             "status": ["INIT", "ENQUEUED", "RUNNING", "DONE", "ERROR", "DEAD", "CANCELLED"],
#         }
#         response = self.bs.session.post(url, json=json_data)
#
#         if all([response.status_code == 200, response.json().get("code") == "OK"]):
#             tasks = response.json().get("data", dict()).get("tasks")
#             return tasks[0] if tasks and tasks[0].get("status") in ["DONE", "ERROR", "DEAD", "CANCELLED"] else None
#         else:
#             self.bs.logger.exception("获取任务队列失败")
#
#     def get_queues(self):
#         schedule_list = Schedule.objects.filter(is_status=0, is_handle=1, is_del=0, status="ON").values_list(
#             "schedule_id")
#         for sd in schedule_list:
#             self.analysis_queue(self.get_queue(sd[0]))
#
#     @staticmethod
#     def save_queue(data: dict):
#         Queue.objects.update_or_create(task_id=data.get("task_id"), schedule_id=data.get("schedule_id"), defaults=data)
#
#     @staticmethod
#     def cal_time(time1: [str, datetime.datetime], time2: [str, datetime.datetime], flag=False):
#         """
#         计算时间差
#         :param flag:
#         :param time1:开始时间
#         :param time2:结束时间
#         :return:
#         """
#         if isinstance(time1, str):
#             time1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
#         if isinstance(time2, str):
#             time2 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
#         if time2 is None:
#             return 0
#         if time1 > time2:
#             raise ValueError("时间填写反了")
#         seconds = (time2 - time1).seconds
#         if flag:
#             if seconds < 60:
#                 time_str = "{0}秒".format(seconds)
#             elif seconds < 3600:
#                 time_str = "{0}分{1}秒".format(seconds // 60, seconds % 60)
#             else:
#                 time_str = "{0}时{1}分{2}秒".format(seconds // 3600, seconds % 3600 // 60, seconds % 3600 % 60)
#         else:
#             time_str = seconds
#         return time_str
#
#     def analysis_queue(self, queue_data):
#         """
#         解析queue队列
#         :param queue_data:
#         :return:
#         """
#         if queue_data:
#             if queue_data.get("task_type") == "Shovel":
#                 project_class = json.loads(queue_data.get("command")).get("class").split(".")
#                 project = json.loads(queue_data.get("command")).get("project")
#             else:
#                 project_class = [queue_data.get("command")]
#                 project = project_class
#             queue_dict = {
#                 "task_id": queue_data.get("task_id"),
#                 "schedule_id": queue_data.get("schedule_id"),
#                 "status": queue_data.get("status"),
#                 "project": project,
#                 "shovel": project_class[0] if len(project_class) == 2 else None,
#                 "shovel_name": project_class[1] if len(project_class) == 2 else project_class[0],
#                 "apply_time": queue_data.get("apply_time"),
#                 "enqueue_time": queue_data.get("enqueue_time"),
#                 "execute_time": queue_data.get("execute_time"),
#                 "finish_time": queue_data.get("finish_time"),
#                 "take_time": self.cal_time(queue_data.get("apply_time"), queue_data.get("finish_time")),
#                 "target_machine": queue_data.get("target_machine"),
#                 "request_user": queue_data.get("request_user"),
#                 "log_of_shovel_task": queue_data.get("log_url_dict").get("log_of_shovel_task"),
#                 "log_of_loop_task": queue_data.get("log_url_dict").get("log_of_loop_task"),
#                 "log_of_loop_task_pipe": queue_data.get("log_url_dict").get("log_of_loop_task_pipe"),
#                 "schedule_name": queue_data.get("schedule_name"),
#             }
#             self.save_queue(queue_dict)
#
#     def get_schedule(self, json_data):
#         """
#         获取定时任务列表
#         :param json_data:
#         :return:
#         """
#         url = "https://elihu-miner.leqee.com/api/ScheduleController/fetchScheduleList"
#         response = self.bs.session.post(url, json=json_data, timeout=60 * 5)
#         if all([response.status_code == 200, response.json().get("code") == "OK"]):
#             data = response.json().get("data", dict())
#         else:
#             data = {}
#         return data
#
#     def get_schedule_params(self, title=None, status=None, page=None):
#         """
#         获取定时任务
#         :param self:
#         :param page:
#         :param status:状态
#         :param title:
#         :return:
#         """
#         flag, page_size, num = any([title, status]), 40, 0
#         total_page = new_page = page if page else 1
#         json_data = {"page": new_page, "page_size": page_size}
#         json_data.update({"title": title}) if title else None
#         json_data.update({"status": status if status else ["ON", "OFF", "NEVER"]})
#         # item_num = SchedulePage.objects.last()
#         # if not item_num:
#         #     json_data["page"] = 1
#         # elif item_num == page_size:
#         #     json_data["page"] = item_num.page_num + 1
#         # else:
#         #     json_data["page"] = item_num.page_num
#         while json_data.get("page") <= total_page:
#             try:
#                 data = self.get_schedule(json_data)
#                 if data:
#                     self.bs.logger.info("正在获取第{0:0>4d}页".format(json_data["page"]))
#                     total_page, num = math.ceil(data.get("total", 0) / page_size), 0
#
#                     data = data.get("schedules", list())
#                     list(map(self.save_schedule, data))
#                     if not flag:
#                         SchedulePage.objects.update_or_create(page_num=json_data["page"],
#                                                               defaults={"item_num": len(data)})
#                     json_data["page"] += 1
#                 elif num > 3:
#                     raise PermissionError("获取定时任务数据失败")
#                 else:
#                     pass
#             except Exception as e:
#                 self.bs.logger.error(e)
#             finally:
#                 num += 1
#                 time.sleep(random.randint(3, 5))
#
#     def save_schedule(self, data: dict):
#         """
#         储存定时任务信息
#         :param data:
#         :return:
#         """
#         if data.get("job_type") == "Shovel":
#             project_class = json.loads(data.get("command")).get("class").split(".")
#             if len(project_class) == 2:
#                 project_class_shovel = project_class[1]
#                 project_class = project_class[0]
#             else:
#                 project_class_shovel = project_class[0]
#                 project_class = None
#             project = json.loads(data.get("command")).get("project")
#         else:
#             project_class = None
#             project_class_shovel = data.get("command")
#             project = project_class
#         new_data = {
#             "schedule_id": data.get("schedule_id"),
#             "cron_expression": data.get("cron_expression"),
#             "job_code": data.get("job_code"),
#             "target_machine": data.get("target_machine"),
#             "is_status": data.get("is_del"),
#             "status": data.get("status"),
#             "request_user": data.get("request_user"),
#             "project": project,
#             "project_class": project_class,
#             "project_class_shovel": project_class_shovel,
#             "is_handle": self.get_responsible_schedule(project_class)
#         }
#         Schedule.objects.update_or_create(schedule_id=new_data.get("schedule_id"), defaults=new_data)
#
#     @staticmethod
#     def get_responsible_schedule(project_class):
#         responsible_schedule = ResponsibleSchedule.objects.filter(platform_en=project_class).count()
#         return responsible_schedule
#
#     def _add_schedule(self, func, func_id, hour, minute, prompt=True):
#         self.add_job(func=func, id=func_id, trigger="cron", hour=hour, minute=minute,
#                      replace_existing=True, misfire_grace_time=1000 * 90)
#         if prompt:
#             self.bs.logger.info(
#                 "执行[{0}]定时任务启动：{1}时{2}分".format(self.get_job(func_id).id, hour, minute))
#
#     def deal_log(self):
#         qi = Queue.objects.filter(is_check_log=False).values_list("log_of_shovel_task")
#         for job in qi:
#             content = self.get_log(job[0].replace("?use_highlight=YES", ""))
#             if content:
#                 self.analysis_page(content)
#
#         pass
#
#     def get_log(self, url):
#         print(url)
#         try:
#             response = self.bs.session.get(url, timeout=60 * 5)
#         except Exception as e:
#
#             response = self.bs.session.get(url, timeout=60 * 5)
#         time.sleep(random.randint(2, 3))
#         if response.status_code == 200:
#             return response.text
#         else:
#             self.bs.logger.error("此链接获取失败：{0}".format(url))
#
#     def analysis_page(self, text):
#         """
#         解析日志内容
#         :param text:
#         :return:
#         """
#         try:
#             task_id = re.findall("detail-(\\d+)", text)[0]
#             contents = re.findall("Mizar record ID:(\\d+).*\\|(.*)", text)
#
#             for content in contents:
#                 new_dict = json.loads(content[1])
#                 new_dict = {
#                     "task_id": task_id,
#                     "part_key": new_dict.get("part_key"),
#                     "epitaph": new_dict.get("epitaph"),
#                     "target_table": new_dict.get("target_table"),
#                     "mizar_id": content[0],
#                     "feedback": new_dict.get("feedback"),
#                 }
#                 QueueLog.objects.update_or_create(task_id=new_dict.get("task_id"), mizar_id=new_dict.get("mizar_id"),
#                                                   defaults=new_dict)
#         except Exception as e:
#             print(text)
#             # DingRobot().send_request("解析数据出错")
#             self.bs.logger.error("解析数据出错：{0}".format(e))
#
#     def run(self):
#         self.deal_log()
#         self._add_schedule(self.get_schedule_params, func_id="schedule", hour=16, minute=10)
#         self._add_schedule(self.get_queues, func_id="queue", hour=17, minute=10)
#         self._add_schedule(self.deal_log, func_id="queue", hour=17, minute=10)
#         self.start()
