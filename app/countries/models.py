from django.db import models


# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Country')

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class OriginCountry(models.Model):
    origin_country = models.ForeignKey(
        Country, related_name="origins",  on_delete=models.CASCADE
    )
    destinations = models.ManyToManyField(
        Country, related_name="destinations", through="BorderStatus"
    )

    @property
    def origin_country_name(self):
        return self.origin_country.name

    class Meta:
        verbose_name_plural = "Origin Countries"

    def __str__(self):
        return self.origin_country.name

class BorderStatus(models.Model):
    STATUS_CHOICES = [("OP", "OPEN"), ("SEMI", "CAUTION"), ("CLOSED", "CLOSED")]
    origin_country = models.ForeignKey(OriginCountry, on_delete=models.CASCADE, default=None)
    destination = models.ForeignKey(Country, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default="CLOSED")
    extra = 1
    class Meta:
        unique_together = [("destination", "origin_country")]
        verbose_name_plural = "Border Statuses"

    def __str__(self):
        return (
            f"{self.origin_country.origin_country.name} -> {self.destination.name}"
            f" ({self.status})"
        )
