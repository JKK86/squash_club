from django.db import models

from squash_club import settings


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name="Nazwa")
    slug = models.SlugField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "kategorię"
        verbose_name_plural = "Kategorie"


class Court(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courts", verbose_name="Kategoria")
    number = models.PositiveIntegerField(verbose_name="Numer kortu")
    air_condition = models.BooleanField(default=False, verbose_name="Klimatyzacja")
    lighting = models.BooleanField(default=True, verbose_name="Oświetlenie")

    def __str__(self):
        return f"Kort nr {self.number}"

    class Meta:
        verbose_name = "kort"
        verbose_name_plural = "Korty"
        ordering = ("number", )


class Reservation(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="reservations", verbose_name="Kort")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Użytkownik")
    date = models.DateField(verbose_name="Data rezerwacji")
    time = models.TimeField(verbose_name="Godzina rezerwacji")
    duration = models.PositiveIntegerField(verbose_name="Czas rezerwacji", default=1)
    paid = models.BooleanField(default=False, verbose_name="Opłacone")
    status = models.BooleanField(default=False, verbose_name="Status")
    comments = models.TextField(verbose_name="Komentarz", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    def __str__(self):
        return f"Rezerwacja nr {self.id}"

    class Meta:
        verbose_name = "rezerwacja"
        verbose_name_plural = "Rezerwacje"
        constraints = [models.UniqueConstraint(fields=["court", "date", "time"], name="unique_reservation")]
