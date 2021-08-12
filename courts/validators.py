from django.core.exceptions import ValidationError
import re


def validate_phone_number(phone_number):
    pattern = r'^\d{3} *\d{3} *\d{3}$'
    if not re.fullmatch(pattern, phone_number):
        raise ValidationError("Nieprawidłowy numer telefonu. Podaj numer w formacie: 111 111 111")