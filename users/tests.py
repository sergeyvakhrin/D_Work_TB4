from django.urls import reverse
from eventlet.green.http.client import responses
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.data = {
            'phone': '+71111111111',
        }
        self.referral_1 = 'rrrrr1'
        self.referral_2 = 'rrrrr2'
        self.sms_code = '1234'

    def test_user_create_1(self):
        """ Проверяем создание уникального пользователя """
        # url = reverse('users:sms_auth') # TODO: тест не проходит с ошибкой  phone = request._post.get('phone')
        response = self.client.post('/api/authsms/auth/sms/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 1)

        response = self.client.post('/api/authsms/auth/sms/', data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(), 1)

    def test_first_user_is_superuser(self):
        """ Проверяем первого пользователя на права администратора """
        response = self.client.post('/api/authsms/auth/sms/', data=self.data)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(pk=1)
        self.assertEqual(user.is_superuser, True)

    def test_list_api(self):
        url = reverse('users:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

