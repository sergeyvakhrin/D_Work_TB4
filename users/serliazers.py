import secrets

from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User, Referral
from users.servises import send_sms


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
        # Исключаем поля для frontend
        exclude = ('id', 'password', 'last_login', 'is_active', 'date_joined', 'groups', 'user_permissions',
                   'is_staff', 'is_superuser',)

    def validate_user_referral(self, value):
        """ Если user_referral уже вводился, генерирует ошибку """
        referral = Referral.objects.filter(referral=value)
        if referral is None:
            raise APIException("Such referral does not exist.")
        if self.instance.user_referral:
            raise APIException("You may not edit user_referral.")
        return value

    def validate_self_referral(self, value):
        """ Генерирует ошибку при попытке изменения self_referral """
        if self.instance.self_referral:
            raise APIException("You may not edit self_referral.")
        return value

    def validate_phone(self, value):
        """ Отправка смс при смене номера телефона """
        if str(self.instance) != value:
            # Получаем объект у которого меняется номер телефона
            user = self.instance
            # Получаем смс-код на новый телефон
            sms_password = send_sms(value)
            user.sms_code = sms_password + value

            # TODO: При PUT запросе на /update/pk/ профиля, если вводится новый номер телефона, высылается смс на новый
            # TODO: телефон, но сам телефон не меняется. И при PUT запросе на /update/sms/pk/ передается новый телефон
            # TODO: и смс-код. Если смс-код верный, то телефон меняется.

            user.set_password(sms_password)
            user.save()
            return str(self.instance)
        else:
            return str(self.instance)

    def get_users_list(self, instance):
        """
        Выводит список пользователей (номера телефонов),
        которые ввели реферальный код текущего пользователя.
        """
        users_list = User.objects.filter(user_referral=instance.self_referral)
        return [user.phone for user in users_list]

    # def get_user_referral(self, instance):
    # """ Для получения данных из связанной таблицы """
    #     return User.objects.get(user_referral=instance.user_referral)


class UserPhoneUpdateSerializer(serializers.ModelSerializer):
    """ Сериалайзер для смены номера телефона профиля """
    class Meta:
        model = User
        fields = ('phone', 'sms_code', )

    def validate_phone(self, value):
        """ Проверяет вводимую пару смс-код и номер телефона """
        user = self.instance
        sms_code = self.initial_data['sms_code']
        if user.sms_code == sms_code + value:
            return value
        raise APIException("Incorrect phone/sms pair.")
