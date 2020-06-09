from django.db import models
from django.utils.datetime_safe import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import MyUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


class EmployeeProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, verbose_name=_("Pracownik"))
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Adres"))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Numer telefonu musi być podany w formacie: '+999999999'. Maksymalnie 15 cyfr")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                    blank=True, null=True,
                                    verbose_name=_("Numer telefonu"))  # validators should be a list

    class Meta:
        verbose_name = _('Profil pracownika')
        verbose_name_plural = _('Profile pracowników')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=MyUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            #if instance.is_superuser or instance.is_staff:
            EmployeeProfile.objects.using(settings.ADMIN_DB).create(user=instance)

    @receiver(post_save, sender=MyUser)
    def save_user_profile(sender, instance, **kwargs):
        #if instance.is_superuser or instance.is_staff:
        instance.employeeprofile.save()


class Position(models.Model):
    name = models.CharField(max_length=200,verbose_name=_("Nazwa"))

    class Meta:
        verbose_name = _('Stanowisko')
        verbose_name_plural = _('Stanowiska')

    def __str__(self):
        return self.name


class EmployeePosition(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_("Pozycja"))
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Pracownik"))

    class Meta:
        verbose_name = _('Stanowisko-Pracownik')
        verbose_name_plural = _('Stanowiska-Pracownicy')

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_("Stanowisko"))
    text = models.CharField(max_length=200, verbose_name=_("Treść"))
    dt_created = models.DateTimeField(default=datetime.now,verbose_name=_("Data wysłania"))

    class Meta:
        verbose_name = _('Notyfikacja SMS')
        verbose_name_plural = _('Notyfikacje SMS')

    def __str__(self):
        return self.name
