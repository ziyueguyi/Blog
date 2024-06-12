"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from Back.views import BackView, DealIframeView
from Login.views import LoginView
from Main.views import MainView

urlpatterns = [
    path('', MainView.as_view()),
    path('back/', BackView.as_view()),
    path('login/', LoginView.as_view()),
    path('back/iframe/', DealIframeView.as_view(), name='iframe'),
]
handler404 = "PubFunc.mixins.page_not_found"
