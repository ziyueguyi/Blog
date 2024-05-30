from django.shortcuts import render

from PubFunc.mixins import UserAPIView


# Create your views here.
class MainView(UserAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        # template = request.query_params.get('template')
        return render(request, "main.html")


def page_not_found(request, exception=None):
    return render(request, 'main.html', status=404)
