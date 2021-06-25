from django.db import models


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

