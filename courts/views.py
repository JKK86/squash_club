import datetime

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View

from courts.forms import ReserveCourtForm, AddPhoneNumberForm
from courts.models import Reservation, PriceList, Court, Notification, Category
from courts.tasks import reservation_confirm, send_sms_notification
from users.models import Profile

User = get_user_model()


class ScheduleView(View):
    def get(self, request):
        present = datetime.date.today()
        dates = []
        day = datetime.timedelta(days=1)
        for i in range(7):
            dates.append(present + i * day)
        prices = PriceList.objects.filter(weekend=False)
        weekend_price = PriceList.objects.get(weekend=True)
        return render(request, 'schedule.html', {"dates": dates, "prices": prices, "weekend_price": weekend_price})


class ReserveView(View):
    def get(self, request, year, month, day, hour):
        date = datetime.date(year, month, day)
        time = datetime.time(hour)
        form = ReserveCourtForm(date, time)
        if date.strftime("%A") in ["Sobota", "Niedziela"]:
            price = PriceList.objects.get(weekend=True)
        else:
            price = PriceList.objects.get(time=time.strftime("%-H"))
        return render(request, 'reserve_court.html', {'form': form, 'date': date, 'time': time, 'price': price})

    def post(self, request, year, month, day, hour):
        date = datetime.date(year, month, day)
        time = datetime.time(hour)
        user = request.user
        form = ReserveCourtForm(date, time, request.POST)
        if date.strftime("%A") in ["Sobota", "Niedziela"]:
            price = PriceList.objects.get(weekend=True)
        else:
            price = PriceList.objects.get(time=time.strftime("%-H"))
        if form.is_valid():
            court = form.cleaned_data['court']
            discount = form.cleaned_data['discount']
            comment = form.cleaned_data['comment']
            if discount:
                total_price = price.price - discount.discount
            else:
                total_price = price.price
            reservation = Reservation.objects.create(
                court=court,
                user=user,
                date=date,
                time=time,
                # duration=duration,
                price=total_price,
                comment=comment
            )
            reservation_confirm.delay(reservation.id)
            return render(request, "reservation_confirm.html", {'reservation': reservation})
        else:
            return render(request, 'reserve_court.html', {'form': form, 'date': date, 'time': time, 'price': price})


class CancelReservationView(View):
    def post(self, request, reservation_id):
        reservation = Reservation.objects.get(pk=reservation_id)
        user = request.user
        now = datetime.datetime.now()
        date = reservation.date
        time = reservation.time
        if user == reservation.user and now + datetime.timedelta(hours=24) <= datetime.datetime.combine(
                date, time):
            if not Court.objects.exclude(reservations__date=date, reservations__time=time):
                notification = Notification.objects.filter(date=datetime.datetime.combine(date, time)).first()
                if notification:
                    send_sms_notification.delay(notification.id)
                    notification.delete()
            reservation.delete()
        else:
            messages.warning(request,
                             "Nie można anulować tej rezerwacji "
                             "- zostało mniej niż 24 godziny lub użytkownik nie ma uprawnień")
        return redirect('user_profile')


class AddNotificationView(View):
    def get(self, request, category_slug, year, month, day, hour):
        date = datetime.date(year, month, day)
        time = datetime.time(hour)
        user = request.user
        form = AddPhoneNumberForm(initial={"phone_number": user.profile.phone_number})
        return render(request, 'notification_form.html', {"date": date, "time": time, "form": form})

    def post(self, request, category_slug, year, month, day, hour):
        date = datetime.date(year, month, day)
        time = datetime.time(hour)
        category = Category.objects.get(slug=category_slug)
        user = request.user
        profile = Profile.objects.get(user=user)
        form = AddPhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            if phone_number != user.profile.phone_number:
                profile.phone_number = phone_number
                profile.save()
            Notification.objects.create(user=user, category=category, date=datetime.datetime.combine(date, time))
            messages.info(request, "Powiadomimy Cię, jak tylko zwolni się kort w wybranym przez Ciebie terminie.")
        return redirect('schedule')