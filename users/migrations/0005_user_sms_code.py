# Generated by Django 5.1.3 on 2024-12-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_user_self_referral"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="sms_code",
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]