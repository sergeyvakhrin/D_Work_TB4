import secrets

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User, Referral
from users.serliazers import PhoneSerializer


class SMSAuthenticationView(APIView):
    """  """

    def post(self, request):
        """  """
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # Проверяем, есть ли телефон в базе данных
        user = User.objects.filter(phone=phone).exists()
        if user:
            # Если телефон существует, отправляем SMS
            print('send_sms(phone)')
            return Response({"message": "SMS sent to existing user."}, status=status.HTTP_200_OK)
        else:
            # Если телефона нет, создаем новую запись в базе

            # Создаем реферальную ссылку
            self_referral = secrets.token_hex(3)

            # Проверяем уникальность реферальной ссылки
            referral = Referral.objects.filter(referral=self_referral).exists()
            while referral:
                self_referral = secrets.token_hex(3)
                referral = Referral.objects.filter(referral=self_referral).exists()

            # Создаем запись в базе реферальных ссылок
            Referral.objects.create(referral=self_referral)

            # Создаем пользователя с новым телефоном и реферальной ссылкой
            User.objects.create(
                phone=phone,
                self_referral=Referral.objects.get(referral=self_referral)
            )
            print('send_sms(phone)')
            return Response({"message": "User created and SMS sent."}, status=status.HTTP_201_CREATED)

