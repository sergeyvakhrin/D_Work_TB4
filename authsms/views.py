import secrets

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView
from rest_framework.reverse import reverse_lazy

from authsms.forms import UserRegisterForm, UserProfileForm, UserChangePhoneForm
from users.models import User
from users.servises import user_validation, send_sms


def home(request):
    """ Контроллер стартовой страницы """
    context = {}
    return render(request, 'authsms/home.html', context)


class RegisterView(CreateView):
    """ Контроллер регистрации номера телефона на ресурсе """
    model = User
    form_class = UserRegisterForm
    template_name = 'authsms/register.html'

    def post(self, request, *args, **kwargs):
        """ Метод для проверки существования введенного номера телефона """
        phone = request._post.get('phone')
        user_validation(phone)
        return redirect(reverse('authsms:login'))


def logout_view(request):
    """ Функция для кастомного выходы из сервиса """
    # Подменяем пароль, что бы по старой смс не было возможности зайти
    user = request.user
    user.set_password(secrets.token_hex(16))
    user.save()
    logout(request)
    return redirect('/')


class UserProfileView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Класс для просмотра и редактирования профиля пользователя """
    model = User
    form_class = UserProfileForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy('authsms:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        """ Метод для отлавливания изменения телефона профиля пользователем """
        user = self.request.user
        user_phone = user.phone
        print(user.pk)
        input_phone = request._post.get('phone')

        # Отлавливаем изменение номера телефона
        if user.phone != input_phone:
            self.request.session['input_phone'] = input_phone #Для передачи введенного номера телефона в следующую форму
            print("Изменился номер телефона")
            sms_code = send_sms(input_phone)
            user.sms_code = sms_code + input_phone
            user.phone = user_phone
            user.save()
            return redirect('authsms:user_update', pk=user.pk)
        return super().post(self, request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Класс для подтверждения изменения номера телефона профиля """
    model = User
    form_class = UserChangePhoneForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy('authsms:sms_auth')  # TODO: При смене номера телефона в базе слетает авторизация.
                                                    # Нужно как-то это исправить

    def get_form_class(self):
        """ Устраняем возможность редактирования телефона при ручном введении в адресной строке """
        user = self.request.user
        if user == self.object:
            return UserChangePhoneForm
        raise PermissionDenied

    def get_initial(self):
        """ Для передачи введенного номера телефона в следующую форму """
        initial = super().get_initial()
        input_phone = self.request.session.get('input_phone', None)
        if input_phone:
            initial.update({'input_phone': input_phone})
        return initial
