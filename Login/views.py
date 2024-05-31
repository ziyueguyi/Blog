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

    # def get(self, request, *args, **kwargs):
    #     print(request.build_absolute_uri())
    #     return render(request, "login.html")
