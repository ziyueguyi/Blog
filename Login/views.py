from django.shortcuts import render

from PubFunc.mixins import UserAPIView


# Create your views here.
class LoginView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)