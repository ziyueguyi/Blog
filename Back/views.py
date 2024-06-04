from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from Back.models import BackPageUrl, Status
from Back.serializers import BackPageUrlSerializer, StatusSerializer
from PubFunc.mixins import UserAPIView, StatusView


# Create your views here.
class BackView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_table = BackPageUrl
        self.serializer = BackPageUrlSerializer

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
        data = Paginator(data, page_size, allow_empty_first_page=False)
        num_page = data.num_pages
        ser_data = self.serializer(instance=data.page(page).object_list, many=True).data if num_page > 0 else []
        return Response({"page_total": num_page, "page_size": len(ser_data), "data": ser_data, **StatusView.get(3000)},
                        status=status.HTTP_200_OK)


