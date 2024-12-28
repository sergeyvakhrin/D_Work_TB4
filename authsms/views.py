from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, UpdateView, TemplateView
from rest_framework.reverse import reverse_lazy

from users.models import User


def home(request):
    """ Контроллер стартовой страницы """
    context = {}
    return render(request, 'authsms/home.html', context)
