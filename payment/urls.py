from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.PaymentProcessView.as_view(), name="payment_process"),
    path('done/', views.payment_done, name="payment_done"),
    path('cancelled/', views.payment_cancelled, name="payment_cancelled"),
]
