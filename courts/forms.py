import django.forms as forms

from courts.models import Court


class ReserveCourtForm(forms.Form):
    court = forms.ModelChoiceField(Court.objects.all())
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, date, time, *args, **kwargs):
        super(ReserveCourtForm, self).__init__(*args, **kwargs)
        self.fields['court'].queryset = Court.objects.exclude(reservations__date=date, reservations__time=time)
