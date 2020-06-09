from django.db import models
from main.models import MyUser
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Message(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    text = models.TextField(verbose_name=_("Treść"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))

    class Meta:
        verbose_name = _('Wiadomość')
        verbose_name_plural = _('Wiadomości')

    def __str__(self):
        return f'{self.dt_created} - {self.user.username}'
