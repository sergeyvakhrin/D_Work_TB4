from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.models import Referral, User


class AuthSMSTestCase(TestCase):

    def SetUp(self):
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
        self.client.force_authenticate(user=self.user)

    def test_home(self):
        """ Проверяет ответ главной страницы """
        url = reverse('authsms:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


