from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serliazers import PhoneSerializer, UserSerializer, MyTokenObtainPairSerializer, UserPhoneUpdateSerializer
from users.servises import user_validation, IsOwner


class SMSAuthenticationView(APIView):
    """ Кастомный контроллер обработки пути /auth/sms/ """
    def post(self, request):
        """ Проверяет пользователя в базе и отправляет смс """

        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        response = user_validation(phone)
        return response


class MyTokenObtainPairView(TokenObtainPairView):
    """ Кастомный контроллер для сброса пароля после авторизации """
    serializer_class = MyTokenObtainPairSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Обновление профиля пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class UserDeleteAPIView(generics.DestroyAPIView):
    """ Удаление пользователя """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class UserListAPIView(generics.ListAPIView):
    """ Получение списка пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )


class PhoneUpdateAPIView(generics.UpdateAPIView):
    """ При смене телефона приходит подтверждающая смс и нужно ввести на update/sms/{id}/ """
    serializer_class = UserPhoneUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
