from django.core.management import BaseCommand

from users.models import User, Referral


class Command(BaseCommand):
    """ Команда создания Суперюзера """
    def handle(self, *args, **options):

        referral = Referral.objects.create(
            referral='111111'
        )
        referral.save()

        user = User.objects.create(
            phone='+78888888888',
            email='admin@sky.pro',
            self_referral=Referral.objects.get(referral='111111'),
            first_name='Admin',
            last_name='SkyPro',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password('1234')
        user.save()
