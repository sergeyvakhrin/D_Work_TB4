from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from users.models import User


class UserRegisterForm(ModelForm):
    """ Класс создания форму ввода номера телефона """
    class Meta:
        model = User
        fields = ('phone', )