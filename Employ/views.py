from urllib.parse import urlparse

from django.shortcuts import render

from .models import AppList
from PubFunc.mixins import UserAPIView
from .serializers import AppListSerializer


# Create your views here.
class AppListView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_table = AppList
        self.serializer = AppListSerializer

    def get(self, request, *args, **kwargs):
        url_path = urlparse(request.build_absolute_uri()).path.replace("/", "")
        url_path = url_path if url_path else "main"
        return render(request, "back/employ/{0}.html".format(url_path))
