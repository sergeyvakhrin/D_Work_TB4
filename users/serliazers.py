import secrets

from kombu.pools import reset
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Referral


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Кастомный сериализатор для сброса пароля после авторизации """
    def validate(self, attrs):
        data = super().validate(attrs)

        # Дополнительные поля помимо токенов
        data['phone'] = self.user.phone

        # Сбрасываем пароль, что бы по предыдущей смс не было возможности зайти
        reset_password = secrets.token_hex(16)
        print(reset_password)
        self.user.set_password(reset_password)
        self.user.save()
        return data


class PhoneSerializer(serializers.Serializer):
    """ Задаем поле для телефона """
    phone = serializers.CharField(max_length=35)


class UserSerializer(serializers.ModelSerializer):
    users_list = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = '__all__'
        # Исключаем поля для frontend
        exclude = ('id', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def get_users_list(self, instance):
        """
        Выводит список пользователей (номера телефонов),
        которые ввели реферальный код текущего пользователя.
        """
        users_list = User.objects.filter(user_referral=instance.self_referral)
        return [user.phone for user in users_list]