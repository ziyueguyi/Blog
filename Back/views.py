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
        ser_data = self.serializer(instance=self.db_table.objects.all(), many=True).data
        return Response({"data": ser_data, **StatusView.get(200)}, status=status.HTTP_200_OK)


class DealIframeView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_table = BackPageUrl
        self.serializer = BackPageUrlSerializer

    def get(self, request, *args, **kwargs):
        params = request.GET.get('s_id', 10)
        ser_data = self.serializer(instance=self.db_table.objects.filter(ID=params).first()).data
        return render(request, "back/{0}.html".format(ser_data.get("page_url", "home_page")))
