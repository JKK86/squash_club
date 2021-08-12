from django.urls import path
from . import views

urlpatterns = [
    path('schedule/', views.ScheduleView.as_view(), name="schedule"),
    path('reservation/<int:year>/<int:month>/<int:day>/<int:hour>/', views.ReserveView.as_view(),
         name="reserve_court"),
    path('cancel_reservation/<int:reservation_id>/', views.CancelReservationView.as_view(), name="cancel_reservation"),
    path('notification/<slug:category_slug>/<int:year>/<int:month>/<int:day>/<int:hour>/',
         views.AddNotificationView.as_view(), name="add_notification"),
]
