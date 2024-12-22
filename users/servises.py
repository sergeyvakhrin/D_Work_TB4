import secrets
import time

from users.models import Referral


def send_sms(phone):
    """ Функция получения смс с задержкой 2 секунды """
    time.sleep(2)
    print(f'send_sms {phone}') # TODO: реализовать с помощью https://smsaero.ru/integration/api/
    return '1234'

def get_valid_self_referral():
    """ Генерируем и проверяем на уникальность реверальную ссылку """
    referral = True
    while referral:
        # Создаем реферальную ссылку
        self_referral = secrets.token_hex(3)
        referral = Referral.objects.filter(referral=self_referral).exists()
    return self_referral
