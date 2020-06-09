from django.db import models
from django.utils.datetime_safe import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'main_custom_user_table_name'
        verbose_name = _('Użytkownik')
        verbose_name_plural = _('Użytkownicy')

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Adres"))
    loyalty_points = models.IntegerField(default=0, verbose_name=_("Punkty lojalnościowe"))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True, verbose_name=_("Numer telefonu"))  # validators should be a list

    class Meta:
        verbose_name = _('Profil użytkownika')
        verbose_name_plural = _('Profile użytkowników')

    def __str__(self):
        return self.user.username

    """
    @receiver(post_save, sender=MyUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.is_superuser or instance.is_staff:
                return
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=MyUser)
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_superuser or instance.is_staff:
            return
        instance.userprofile.save()
    """




