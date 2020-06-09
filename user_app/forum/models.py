from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import gettext_lazy as _
from main.models import MyUser
# Create your models here.


class Topic(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    title = models.CharField(max_length=200, verbose_name=_("Tytuł"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))
    dt_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_("Data usunięcia"))

    class Meta:
        verbose_name = _('Temat')
        verbose_name_plural = _('Tematy')

    def __str__(self):
        return self.title


class Post(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    forum_topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name=_("Temat"))
    text = models.TextField(verbose_name=_("Treść"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))
    dt_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_("Data usunięcia"))

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posty')

    def __str__(self):
        return f'{self.dt_created} - {self.user.username} - {self.forum_topic.title}'