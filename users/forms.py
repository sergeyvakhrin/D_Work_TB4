from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms

from users.models import User


class UserRegisterForm(ModelForm):
    """ Класс создания формы ввода номера телефона """
    class Meta:
        model = User
        fields = ('phone', )


class UserProfileForm(UserChangeForm):
    """ Класс создания формы для просмотра деталей профиля пользователя """
    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name',  'avatar', 'self_referral', 'user_referral')

    def __init__(self, *args, **kwargs):
        """
        Вводим ограничения на редактирование полей:
        password Что бы скрыть в форме "Пароль не задан"
        self_referral
        user_referral
        """
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
        self.fields['self_referral'].disabled = True

        user = kwargs.get('instance')
        user_referral = user.user_referral
        if user_referral is None:
            self.fields['user_referral'].widget = forms.TextInput(attrs={'class': 'form-control'})
        else:
            self.fields['user_referral'].disabled = True

