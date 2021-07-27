from django import template

from courts.models import Court

register = template.Library()


@register.simple_tag
def check_if_courts_reserved(date, time):
    if Court.objects.exclude(reservations__date=date, reservations__time=time):
        return False
    else:
        return True
