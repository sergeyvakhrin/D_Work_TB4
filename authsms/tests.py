from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class AuthSMSTestCase(TestCase):

    def test_home(self):
        """ Проверяет ответ главной страницы """
        url = reverse('authsms:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
