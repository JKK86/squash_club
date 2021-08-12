import django.forms as forms

from courts.models import Court, Discount
from courts.validators import validate_phone_number


class ReserveCourtForm(forms.Form):
    court = forms.ModelChoiceField(Court.objects.all(), empty_label=None)
    discount = forms.ModelChoiceField(Discount.objects.all(), required=False)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, date, time, *args, **kwargs):
        super(ReserveCourtForm, self).__init__(*args, **kwargs)
        self.fields['court'].queryset = Court.objects.exclude(reservations__date=date, reservations__time=time)


class AddPhoneNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=12, label="Numer telefonu", validators=[validate_phone_number])