from rest_framework import serializers

from users.models import User, Referral


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