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

    # def test_user_create(self):
    #     """ Проверяем создание уникального пользователя """
    #     url = reverse('authsms:sms_auth')
    #     response = self.client.post(url, self.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(User.objects.all().count(), 2)
    #
    #     response = self.client.post(url, self.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(User.objects.all().count(), 2)

    # def test_first_user_is_superuser(self):
    #     """ Проверяем первого пользователя на права администратора """
    #     User.objects.all().delete()
    #     url = reverse('authsms:sms_auth')
    #     response = self.client.post(url, data=self.data)
    #     self.assertEqual(User.objects.all().count(), 1)
    #     user = User.objects.all().first()
    #     self.assertEqual(user.is_superuser, True)

    # def test_profile(self):
    #     """ Проверяем личные данные """

    # def test_update(self):
    #     """ Проверка обновления личных данных """
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     data = {
    #         'email': 'admin@sky.pro',
    #         'first_name': 'Mikula'
    #         }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_phone_unique(self):
    #     """ Проверка обновления номера телефона на уникальность """
    #     User.objects.create(phone=self.data['phone'])
    #
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     response = self.client.put(url, self.data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_phone(self):
    #     """
    #     Проверка обновления номера телефона на уникальный номер.
    #     Номер не должен поменять, пока не будет выполнено смс подтверждение.
    #     """
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     response = self.client.put(url, self.data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(self.user.phone, self.phone)
    #
    #     print(self.user.sms_code) # TODO: 'sms_code': None - полученное значение не присваивается полю ????????????!
    #
    #
    #     sms_code = response.data['sms_code']
    #     data = {
    #         'phone': self.data['phone'],
    #         'sms_code': sms_code[:4]
    #     }
    #     self.user.sms_code = sms_code[:4] + self.data['phone'] # TODO: костыль
    #
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     response = self.client.patch(url, data)
    #     print(vars(self.user))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)  #!!!!!!!!!!!!!!!!!!!!!!!!!
    #     self.assertEqual(self.user.phone, self.data['phone'])       #!!!!!!!!!!!!!!!!!!!!!!!!

    # def test_self_referral(self):
    #     """ Проверка присвоения реферальной ссылки при создании пользователя """
    #     url = reverse('authsms:sms_auth')
    #     response = self.client.post(url, data=self.data)
    #     user = User.objects.get(phone=self.data['phone'])
    #     self.assertEqual(len(user.self_referral_id), 6)

    # def test_user_referral(self):
    #     """
    #     Проверка присвоения реферальной ссылки другого пользователя.
    #     Если уже присвоена, то выдаст ошибку
    #     """
    #     url = reverse('authsms:sms_auth')
    #     response_1 = self.client.post(url, data=self.data)
    #     response_2 = self.client.post(url, data=self.data_2)
    #     user_1 = User.objects.get(phone=self.data['phone'])
    #     user_2 = User.objects.get(phone=self.data_2['phone'])
    #     print(user_1.self_referral_id)
    #     print(user_2.self_referral_id)
    #
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     data = {
    #         "user_referral": str(user_1.self_referral_id),
    #             }
    #     response = self.client.patch(url, data)
    #
    #     self.assertEqual(self.user.user_referral_id, user_1.self_referral_id)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #     data = {
    #         "user_referral": user_2.self_referral_id
    #     }
    #     response = self.client.patch(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)   #!!!!!!!!!!!!!!!!!!!!!!!!
    #     self.assertEqual(self.user.user_referral_id, user_1.self_referral_id)    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    # def test_user_referral_not_exists(self):
    #     """ Проверяет введенный user_referral реферал на существование в базе """
    #     self.user.user_referral = self.user_referral_1
    #
    #     url = reverse('authsms:user_update', args=(self.user.pk,))
    #     data = {
    #         'user_referral': self.user_referral_2
    #     }
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # НЕ РАБОТАЕТ!!!!!!!!!!!!!!!!!!!!!!!!!

    # def test_login(self):
    #     """ Проверяет сброс пароля при входе """
    #     pass                                        # НЕ ПОНИМАЮ, КАК ПРОВЕРИТЬ?????????????!!!!!!!!!!!!
