from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from Back.models import BackPageUrl
from Back.serializers import BackPageUrlSerializer
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
        page = ser_data.get("page_url", "home_page")
        page = page if page else "home_page"
        return render(request, "back/{0}.html".format(page))

    def post(self, request, *args, **kwargs): ...

    def put(self, request, *args, **kwargs): ...

    def delete(self, request, *args, **kwargs): ...

    def options(self, request, *args, **kwargs): ...
