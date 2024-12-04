from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SmallIntegerField

NULLABLE = {"null": True, "blank": True}

class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=35, unique=True, validators="Номер телефона", help_text="Укажите номер телефона")
    email = models.EmailField(max_length=255, verbose_name="Почта", help_text="Укажите почту", **NULLABLE)
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Укажите имя", **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Укажите фамилию", **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatar', verbose_name="Фото", help_text="Загрузите фото", **NULLABLE)
    self_referral = models.OneToOneField('Referral', on_delete=models.CASCADE, verbose_name="Реферал")
    user_referral = models.OneToOneField('Referral', on_delete=models.SET_NULL, verbose_name="Реферальная ссылка", **NULLABLE)
    # sms_code = models.SmallIntegerField(max_length=4, **NULLABLE)


    def __str__(self):
        return self.phone

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Referral(models.Model):
    referral = SmallIntegerField(max_length=6, unique=True, verbose_name="Реферальная ссылка")

    def __str__(self):
        return self.referral

    class Meta:
        verbose_name = "Инвайт-код"
        verbose_name_plural = "Инвайт-коды"