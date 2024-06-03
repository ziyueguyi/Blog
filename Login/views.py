from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from .serializers import UserSerializer
from .models import User
from PubFunc.mixins import UserAPIView


# Create your views here.
class LoginView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_table = User
        self.serializer = UserSerializer

    def options(self, request, *args, **kwargs):
        """
        获取数据列表
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.db_table.objects
        account_info = dict(request.data)
        if ['account', 'password'] == list(account_info.keys()):
            account_info = {k: v[0] for k, v in account_info.items()}
            data = data.filter(**account_info)
            if data.count() == 1:
                response = render(request, 'main.html')
                response.set_cookie(key='have_a_cookie', value=1337)
                return JsonResponse({"code": 200, "msg": "/"})
            else:
                return JsonResponse({"code": 404, "msg": "账号信息错误"})
        else:
            return JsonResponse({"code": 400, "msg": "参数错误"})
