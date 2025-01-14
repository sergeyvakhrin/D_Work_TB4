import secrets
import time
import random

from django.contrib.auth.hashers import make_password
from rest_framework import status, permissions
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from users.models import Referral, User


def send_sms(phone):
    """ Функция получения смс с задержкой 2 секунды """
    time.sleep(2)

    cookies = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    a = random.sample(cookies, 4)
    sms_code = ''.join(a)

    print(f'send_sms {phone}') # TODO: реализовать с помощью https://smsaero.ru/integration/api/
    print(f'sms-code: {sms_code}')
    return sms_code


def get_valid_self_referral():
    """ Генерируем и проверяем на уникальность реферальную ссылку """
    referral = True
    while referral:
        # Создаем реферальную ссылку
        self_referral = secrets.token_hex(3)
        referral = Referral.objects.filter(referral=self_referral).exists()
    return self_referral


def user_validation(phone):
    """ Проверяет пользователя в базе. Если отсутствует, добавляет """

    # Проверяем наличие группы Пользователи
    group_name_for_users = 'users' # TODO: Можно убрать в .env для первоначальных настроек сервиса
    validate_group(group_name_for_users)

    # Если база пользователей пуста, то первый пользователь создается с правами администратора
    permission_staff, permission_superuser = validate_first_user()

    # Проверяем, есть ли телефон в базе данных
    user = User.objects.filter(phone=phone).first()
    if user:
        # Если телефон существует, отправляем SMS
        sms_password = send_sms(phone)
        user.set_password(sms_password)
        user.save()
        return Response({"message": "SMS sent to existing user."}, status=status.HTTP_200_OK)
    else:
        # Если телефона нет, создаем новую запись в базе.
        # Получаем реферальную ссылку для нового пользователя.
        self_referral = get_valid_self_referral()
        # Создаем запись в базе реферальных ссылок
        Referral.objects.create(referral=self_referral)
        # Отправляем смс
        sms_password = send_sms(phone)
        # Создаем пользователя с новым телефоном, реферальной ссылкой и кодом из смс
        User.objects.create(
            phone=phone,
            self_referral=Referral.objects.get(referral=self_referral),
            password=make_password(sms_password),
            is_active=True,
            is_staff=permission_staff,
            is_superuser=permission_superuser
        )
        # Добавляем нового пользователя в группу Users, что бы работали permissions
        user = User.objects.get(phone=phone)
        user.groups.add(Group.objects.get(name=group_name_for_users))
        return Response({"message": "User created and SMS sent."}, status=status.HTTP_201_CREATED)


class IsOwner(permissions.BasePermission):
    """ Проверяем права на просмотр и редактирование."""
    def has_object_permission(self, request, view, obj):
        if obj.phone == request.user.phone:
            return True
        return False


def validate_group(name):
    """
    Проверяем наличие группы Пользователи. Если нет, то создаем с необходимыми правами.
    Новые пользователи будут добавляться в эту группы, что бы работали permissions.
    """
    group = Group.objects.filter(name=name).first()
    if group is None:
        Group.objects.create(name=name)
        group = Group.objects.get(name=name)
        proj_add_perm_1 = Permission.objects.get(name='Can view Пользователь')
        group.permissions.add(proj_add_perm_1)
        proj_add_perm_2 = Permission.objects.get(name='Can change Пользователь')
        group.permissions.add(proj_add_perm_2)


def validate_first_user():
    """ Проверяет наличие пользователей в безе и выдает права is_staff и is_superuser """
    if User.objects.all():
        return False, False
    else:
        return True, True
