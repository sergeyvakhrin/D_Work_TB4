from django.urls import path

from authsms.apps import AuthsmsConfig
from authsms.views import home

app_name = AuthsmsConfig.name

urlpatterns = [
    path('', home, name='home'),

]