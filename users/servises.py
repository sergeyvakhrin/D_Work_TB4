import secrets
import time

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response

from users.models import Referral, User


def send_sms(phone):
    """ Функция получения смс с задержкой 2 секунды """
    time.sleep(2)
    sms_code = '1234'
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
            password=make_password(sms_password)
        )
        return Response({"message": "User created and SMS sent."}, status=status.HTTP_201_CREATED)
