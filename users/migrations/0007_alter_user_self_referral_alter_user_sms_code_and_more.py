# Generated by Django 5.1.3 on 2025-01-02 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_alter_user_sms_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="self_referral",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="self_referral",
                to="users.referral",
                to_field="referral",
                verbose_name="Реферал",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="sms_code",
            field=models.CharField(
                blank=True, help_text="Введите СМС-код", max_length=39, null=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="user_referral",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_referral",
                to="users.referral",
                to_field="referral",
                verbose_name="Реферальная ссылка",
            ),
        ),
    ]