import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from courts.models import Reservation
from users.forms import RegistrationForm
from users.models import Profile

User = get_user_model()


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email']
        )
        profile = Profile.objects.create(user=new_user)
        messages.success(self.request, "Użytkownik został pomyślnie zarejestrowany")
        return super().form_valid(form)


class UserProfileView(View):
    def get(self, request):
        user = request.user
        reservations = Reservation.objects.filter(user=user)
        now = datetime.datetime.now()
        for reservation in reservations:
            if now > datetime.datetime.combine(reservation.date, reservation.time):
                reservation.status = True
            reservation.frozen = now + datetime.timedelta(hours=24) > datetime.datetime.combine(
                    reservation.date, reservation.time)
        return render(request, 'user_profile.html', {'reservations': reservations})

