import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

from courts.forms import ReserveCourtForm
from courts.models import Reservation, PriceList, Court

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
            reservation = Reservation.objects.create(
                court=court,
                user=user,
                date=date,
                time=time,
                # duration=duration,
                price=price.price,
                comment=comment
            )
            return render(request, "reservation_confirm.html", {'reservation': reservation})
        else:
            return render(request, 'reserve_court.html', {'form': form, 'date': date, 'time': time, 'price': price})
