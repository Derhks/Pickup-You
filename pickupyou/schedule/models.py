import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Conductor")
        verbose_name_plural = _("Conductores")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Coordinates(models.Model):
    latitude = models.CharField(max_length=9, verbose_name="Latitud")
    longitude = models.CharField(max_length=9, verbose_name="Longitud")

    class Meta:
        verbose_name = _("Coordenadas")
        verbose_name_plural = _("Coordenadas")

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"


class Order(models.Model):
    title = models.CharField(max_length=150, verbose_name="Titulo")
    day = models.DateField(verbose_name="Día")
    start_time = models.TimeField(verbose_name="Hora de Inicio")
    driver = models.ForeignKey(
        Driver,
        related_name="orders",
        on_delete=models.CASCADE,
        verbose_name="Conductor"
    )
    pickup_point = models.ForeignKey(
        Coordinates,
        related_name='pickup_point',
        on_delete=models.CASCADE,
        verbose_name="Lugar de Recogida")
    destination_point = models.ForeignKey(
        Coordinates,
        related_name='destination_point',
        on_delete=models.CASCADE,
        verbose_name="Lugar de Destino")

    class Meta:
        verbose_name = _("Pedido")
        verbose_name_plural = _("Pedidos")

    def __str__(self):
        return f"{self.title}"

    def set_end_time(self) -> datetime.time:
        tmp_datetime = datetime.datetime.combine(datetime.date(1, 1, 1),
                                                 self.start_time)
        order_duration = datetime.timedelta(hours=1)

        return (tmp_datetime + order_duration).time()

    end_time = models.TimeField(verbose_name="Hora de Finalización")

    def save(self, *args, **kwargs):
        if not self.end_time:
            self.end_time = self.set_end_time()

        super(Order, self).save(*args, **kwargs)
