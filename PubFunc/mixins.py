# -*- coding: utf-8 -*-
"""
# @项目名称 :LargeMarket
# @文件名称 :mixins.py
# @作者名称 :sxzhang1
# @日期时间 :2024/4/30 13:08
# @文件介绍 :
"""
from urllib.parse import urlparse

from django.core.paginator import Paginator
from django.db.models import Model
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

from Back.models import Status
from Back.serializers import StatusSerializer


class UserAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_table = Model
        self.serializer = Serializer
        self.page = 1
        self.page_size = 10

    @staticmethod
    def get(request):
        """
        获取页面
        :param request:
        :return:
        """
        url_path = urlparse(request.build_absolute_uri()).path.replace("/", "")
        url_path = url_path if url_path else "main"
        return render(request, "{0}.html".format(url_path))

    def post(self, request):
        """
        添加数据
        :param request:
        :return:
        """
        data = request.data
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            if serializer.save():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("数据已存在", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("数据格式不正确:{0}".format(serializer.errors), status=status.HTTP_303_SEE_OTHER)

    def put(self, request, pk: list):
        """
        修改数据
        :param request:
        :param pk:
        :return:
        """
        data = self.db_table.objects.get(id=pk)
        serializer = self.serializer(instance=data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, **StatusView.get(200)}, status=status.HTTP_200_OK)

    def delete(self, request, pk: list):
        """
        删除数据
        :param request:
        :param pk:
        :return:
        """
        self.db_table.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        """
        获取数据列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.db_table.objects
        params = dict(request.data)
        page = int(params.pop('page', [self.page])[0])
        page_size = int(params.pop('page_size', [self.page_size])[0])
        for k, v in request.query_params.items():
            if k in ['page', 'page_size']:
                continue
            if isinstance(v, str):
                data = data.filter(**{k: v})
            elif isinstance(v, list):
                data = data.filter(**{"{0}__in".format(k): v})
            elif isinstance(v, tuple):
                data = data.filter(**{"{0}__in".format(k): v})
            else:
                pass
        data = data.all()
        print(data)
        data = Paginator(data, page_size, allow_empty_first_page=False)
        num_page = data.num_pages
        ser_data = self.serializer(instance=data.page(page).object_list, many=True).data if num_page > 0 else []
        return Response({"page_total": num_page, "page_size": len(ser_data), "data": ser_data, **StatusView.get(200)},
                        status=status.HTTP_200_OK)


class StatusView:
    @classmethod
    def get(cls, statu):
        """
        获取数据列表
        :param statu:
        :return:
        """
        data = Status.objects.filter(statu_code=statu)
        if data.count() != 1:
            data = Status.objects.filter(statu_code=509)
        ser_data = StatusSerializer(instance=data.first()).data
        return ser_data


def page_not_found(request, exception=None):
    return render(request, 'main.html', status=404)
