import datetime

from django.shortcuts import render
from django.views import View

from courts.forms import ReserveCourtForm


class ScheduleView(View):
    def get(self, request):
        present = datetime.date.today()
        dates = []
        day = datetime.timedelta(days=1)
        for i in range(7):
            dates.append(present + i * day)
        times = []
        hour = datetime.timedelta(hours=1)
        for i in range(7, 24):
            times.append(datetime.time(i))
        return render(request, 'schedule.html', {"dates": dates, "times": times})


class ReserveView(View):
    def get(self, request, year, month, day, hour):
        date = datetime.date(year, month, day)
        time = datetime.time(hour)
        form = ReserveCourtForm(date, time)
        return render(request, 'reserve_court.html', {'form': form, 'date': date, 'time': time})
