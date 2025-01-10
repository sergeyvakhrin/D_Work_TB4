from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import Referral, User


class AuthSMSTestCase(TestCase):

    def setUp(self):
        self.data = {
            'phone': '+71111111111',
        }
        self.data_2 = {
            'phone': '+71111111112',
        }
        self.user_referral_1 = Referral.objects.create(referral='rrrrr1')
        self.user_referral_2 = 'rrrrr2'
        self.phone = '+78888888888'
        self.user = User.objects.create(phone=self.phone)

    def test_home(self):
        """ Проверяет ответ главной страницы """
        url = reverse('authsms:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_create(self):
        """ Проверяем создание уникального пользователя """
        url = reverse('authsms:sms_auth')
        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(User.objects.all().count(), 2)

        response = self.client.post(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(User.objects.all().count(), 2)

    def test_first_user_is_superuser(self):
        """ Проверяем первого пользователя на права администратора """
        User.objects.all().delete()
        url = reverse('authsms:sms_auth')
        response = self.client.post(url, data=self.data)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.all().first()
        self.assertEqual(user.is_superuser, True)

    def test_update(self):
        """ Проверка обновления личных данных """
        url = reverse('authsms:user_update', args=(self.user.pk,))
        data = {
            'email': 'admin@sky.pro',
            'first_name': 'Mikula'
            }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_update_phone_unique(self):
        """ Проверка обновления номера телефона на уникальность """
        User.objects.create(phone=self.data['phone'])

        url = reverse('authsms:user_update', args=(self.user.pk,))
        response = self.client.put(url, self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
