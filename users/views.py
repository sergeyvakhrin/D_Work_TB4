from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, Referral
from users.servises import send_sms, get_valid_self_referral, user_validation


class RegisterView(CreateView):
    """ Контроллер регистрации номера телефона на ресурсе """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        phone = request._post.get('phone')
        user_validation(phone)
        return redirect(reverse('users:login'))


def logout_view(request):
    logout(request)
    return redirect('/')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user