from django.db import models
from django.utils.datetime_safe import datetime
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from main.models import MyUser


class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nazwa"))

    class Meta:
        verbose_name = _('Marka')
        verbose_name_plural = _('Marki')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Nazwa"))
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name=_("Marka"))
    model = models.CharField(max_length=200, verbose_name=_("Model"))

    class Meta:
        verbose_name = _('Produkt')
        verbose_name_plural = _('Produkty')

    def __str__(self):
        return self.name


class ProductOpinion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Produkt"))
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    text = models.CharField(max_length=200, verbose_name=_("Treść"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))
    dt_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_("Data usunięcia"))

    class Meta:
        verbose_name = _('Opinia')
        verbose_name_plural = _('Opinie')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Offer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Produkt"))
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Cena"))
    quantity = models.PositiveIntegerField(verbose_name=_("Ilość"))
    quantity_available = models.PositiveIntegerField(verbose_name=_("Dostępna ilość"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))
    dt_deleted = models.DateTimeField(null=True, blank=True, verbose_name=_("Data usunięcia"))

    class Meta:
        verbose_name = _('Oferta')
        verbose_name_plural = _('Oferty')

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'


class Discount(models.Model):
    loyalty_points = models.IntegerField(verbose_name=_("Punkty lojalnościowe"))
    percentage = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Procent zniżki"))

    class Meta:
        verbose_name = _('Obniżka')
        verbose_name_plural = _('Obniżki')

    def __str__(self):
        return f'{self.loyalty_points} - {self.percentage}'


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name=_("Użytkownik"))
    dt_created = models.DateTimeField(default=datetime.now, verbose_name=_("Data utworzenia"))
    invoice = models.BooleanField(verbose_name=_("Faktura"))
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, verbose_name=_("Obniżka"))

    class Meta:
        verbose_name = _('Zamówienie')
        verbose_name_plural = _('Zamówienia')

    def __str__(self):
        return f'{self.user.username} - {self.dt_created}'


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_("Zamówienie"))
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name=_("Oferta"))
    # price = models.DecimalField(decimal_places=2) # data duplication
    quantity = models.PositiveIntegerField(verbose_name=_("Ilość"))

    class Meta:
        verbose_name = _('Zamówienie - Pozycja')
        verbose_name_plural = _('Zamówienia - Pozycje')

    def __str__(self):
        return f'{self.order.user.username} - {self.offer.dt_created}'