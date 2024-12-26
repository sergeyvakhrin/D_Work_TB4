from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse

from users.forms import UserRegisterForm
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






    # def form_valid(self, form):
    #     """
    #     Получает введенный номер телефона.
    #     Вызывает функцию отправки смс.
    #     Присваивает пароль для входа.
    #     Если номер телефона еще не введен в базу, присваивает self_referral.
    #     """
    #     user = form.save()
    #     phone = user.phone
    #
    #
    #
    #     # Получаем реферальную ссылку для нового пользователя
    #     self_referral = get_valid_self_referral()
    #     # Создаем запись в базе реферальных ссылок
    #     Referral.objects.create(referral=self_referral)
    #     # Отправляем смс
    #     sms_code = send_sms(phone)
    #     user.set_password(sms_code)
    #     user.self_referral = Referral.objects.get(referral=self_referral)
    #     user.save()
    #     return super().form_valid(form)

def logout_view(request):
    logout(request)
    return redirect('/')
