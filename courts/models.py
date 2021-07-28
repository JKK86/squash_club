import datetime

from django.core.exceptions import ValidationError
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
    number = models.PositiveIntegerField(verbose_name="Numer kortu", unique=True)
    air_condition = models.BooleanField(default=False, verbose_name="Klimatyzacja")
    lighting = models.BooleanField(default=True, verbose_name="Oświetlenie")

    def __str__(self):
        return f"Kort nr {self.number}"

    class Meta:
        verbose_name = "kort"
        verbose_name_plural = "Korty"
        ordering = ("number",)


class PriceList(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="prices", verbose_name="Kategoria")
    weekend = models.BooleanField(default=False)
    time = models.IntegerField(choices=[(x, datetime.time(x)) for x in range(0, 24)],
                               verbose_name="Godzina", null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Cena")

    def __str__(self):
        return f"{self.category}: plan cenowy na godzinę {self.time} {'w weekend' if self.weekend else ''}"

    class Meta:
        verbose_name = "cennik"
        verbose_name_plural = "Plany cenowe"
        constraints = [models.UniqueConstraint(fields=["category", "weekend", "time"], name="unique_price")]
        ordering = ["category", "weekend", "time"]

    def clean(self):
        if self.weekend and self.time:
            raise ValidationError("Cena weekendowa obowiązuje przez cały dzień. Nie podawaj godziny.")
        if not self.weekend and not self.time:
            raise ValidationError("Cena w tygodniu nie jest jednakowa w ciągu dnia. Uzupełnij godzinę.")


class Reservation(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="reservations", verbose_name="Kort")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Użytkownik")
    date = models.DateField(verbose_name="Data rezerwacji")
    time = models.TimeField(verbose_name="Godzina rezerwacji")
    duration = models.PositiveIntegerField(verbose_name="Czas rezerwacji", default=1)
    discount = models.ForeignKey("Discount",
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank="True",
                                 verbose_name="Zniżka",
                                 related_name="reservations")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Cena")
    paid = models.BooleanField(default=False, verbose_name="Opłacone")
    status = models.BooleanField(default=False, verbose_name="Status")
    comment = models.TextField(verbose_name="Komentarz", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    def __str__(self):
        return f"Rezerwacja nr {self.id}"

    class Meta:
        verbose_name = "rezerwacja"
        verbose_name_plural = "Rezerwacje"
        constraints = [models.UniqueConstraint(fields=["court", "date", "time"], name="unique_reservation")]


class Discount(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoria", related_name="discounts")
    name = models.CharField(max_length=32, verbose_name="Nazwa")
    discount = models.PositiveIntegerField(verbose_name="Zniżka")