from rest_framework import serializers

from users.models import User


class PhoneSerializer(serializers.Serializer):
    """ Задаем поле для телефона """
    phone = serializers.CharField(max_length=35)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'