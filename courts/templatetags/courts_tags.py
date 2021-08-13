from django import template

from courts.models import Court

register = template.Library()


@register.simple_tag
def check_if_courts_reserved(date, time):
    if Court.objects.filter(reservations__date=date, reservations__time=time).count() == Court.objects.count():
        return True
    else:
        return False
