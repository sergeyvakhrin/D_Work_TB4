import secrets

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from rest_framework.exceptions import PermissionDenied

from users.forms import UserRegisterForm, UserProfileForm, UserChangePhoneForm
from users.models import User
from users.servises import send_sms, user_validation


class RegisterView(CreateView):
    """ Контроллер регистрации номера телефона на ресурсе """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        """ Метод для проверки существования введенного номера телефона """
        phone = request._post.get('phone')
        user_validation(phone)
        return redirect(reverse('users:login'))


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
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        """ Метод для отлавливания изменения телефона профиля пользователем """
        user = self.request.user
        user_phone = user.phone
        print(user.pk)
        input_phone = request._post.get('phone')

        # TODO: Проверяем уникальность введенного телефона. Если не уникальный, оставляем старый.
        # user_input = User.objects.filter(phone=input_phone).first()
        # if user_input:
        #     # raise forms.ValidationError('The entered phone number is already in use.')
        #     # request._post['phone'] = user.phone

        # Отлавливаем изменение номера телефона
        if user.phone != input_phone:
            print("Изменился номер телефона")
            sms_code = send_sms(input_phone)
            user.sms_code = sms_code + input_phone
            user.phone = user_phone
            user.save()
            return redirect('users:user_update', pk=user.pk)
        return super().post(self, request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Класс для подтверждения изменения номера телефона профиля """
    model = User
    form_class = UserChangePhoneForm
    permission_required = 'users.change_user'
    success_url = reverse_lazy('users:sms_auth')

    def get_form_class(self):
        """ Устраняем возможность редактирования телефона при ручном введении в адресной строке """
        user = self.request.user
        if user == self.object:
            return UserChangePhoneForm
        raise PermissionDenied

