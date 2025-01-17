from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    phone = models.CharField(max_length=35, unique=True, verbose_name="Номер телефона",
                             help_text="Укажите номер телефона", db_index=True)
    email = models.EmailField(max_length=255, verbose_name="Почта", help_text="Укажите почту",
                              **NULLABLE, db_index=True)
    first_name = models.CharField(max_length=50, verbose_name="Имя", help_text="Укажите имя",
                                  **NULLABLE, db_index=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", help_text="Укажите фамилию",
                                 **NULLABLE, db_index=True)
    avatar = models.ImageField(upload_to='users/avatar', verbose_name="Фото", help_text="Загрузите фото",
                               **NULLABLE, db_index=True)
    self_referral = models.OneToOneField('Referral', to_field='referral', on_delete=models.CASCADE,
                                         verbose_name="Реферал", **NULLABLE, related_name='self_referral',
                                         db_index=True)
    user_referral = models.ForeignKey('Referral', to_field='referral', on_delete=models.SET_NULL,
                                      verbose_name="Реферальная ссылка", **NULLABLE, related_name='user_referral',
                                      db_index=True)
    sms_code = models.CharField(max_length=39, help_text="Введите СМС-код", **NULLABLE)

    # TODO: Можно добавить альтернативный телефон для входа и получение кода на email

    def __str__(self):
        return self.phone

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Referral(models.Model):
    referral = models.CharField(max_length=6, unique=True, verbose_name="Реферальная ссылка", db_index=True)

    def __str__(self):
        return self.referral

    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = "Реферал"
