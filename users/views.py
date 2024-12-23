from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, Referral
from users.serliazers import PhoneSerializer, UserSerializer, MyTokenObtainPairSerializer
from users.servises import send_sms, get_valid_self_referral


class SMSAuthenticationView(APIView):
    """ Кастомный контроллер обработки пути /auth/sms/ """
    def post(self, request):
        """ Проверяет пользователя в базе и отправляет смс """
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        # Проверяем, есть ли телефон в базе данных
        user = User.objects.filter(phone=phone).first()
        if user:
            # Если телефон существует, отправляем SMS
            sms_password = send_sms(phone)
            user.set_password(sms_password)
            user.save()
            return Response({"message": "SMS sent to existing user."}, status=status.HTTP_200_OK)
        else:
            # Если телефона нет, создаем новую запись в базе
            # Получаем реферальную ссылку для нового пользователя
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


class MyTokenObtainPairView(TokenObtainPairView):
    """ Кастомный контроллер для сброса пароля после авторизации """
    serializer_class = MyTokenObtainPairSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Обновление профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # def perform_update(self, serializer):
    #     """
    #     Перехватывает передаваемый пользователем user_referral,
    #     проверяет на наличие в базе и связывает с пользователем
    #     """
    #     user = self.request.user
    #     if user.user_referral:
    #         raise APIException('Referral already input.')
    #
    #     input_referral = serializer.validated_data['user_referral']
    #
    #     referral = Referral.objects.filter(referral=input_referral).first()
    #     if not referral:
    #         raise APIException("Referral not found.")
    #     else:
    #         user.user_referral = Referral.objects.get(pk=referral.pk)
    #         user.save()
    #         return Response({"message": "Referral saved."})


class UserDeleteAPIView(generics.DestroyAPIView):
    """ Удаление пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListAPIView(generics.ListAPIView):
    """ Получение списка пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PhoneUpdateAPIView(generics.UpdateAPIView):
    """ При смене телефона приходит подтверждающая смс и нужно ввести на update/sms/<int:pk>/ """
    pass
