from celery import shared_task
from django.core.mail import send_mail


@shared_task
def reservation_confirm(reservation_id):
    """Zadanie wysyłające powiadomienie mailem, po złożeniu rezerwacji"""
    from courts.models import Reservation
    reservation = Reservation.objects.get(pk=reservation_id)
    subject = f"Rezerwacja nr {reservation.id}"
    message = f"Witaj, {reservation.user.first_name}!\n\n" \
              f"Dokonałeś rezerwacji na kort do {reservation.court.category}a " \
              f"na dzień {reservation.date} o godzinie {reservation.time}. Twój kort to {reservation.court}.\n" \
              f"Życzymy udanej gry!"
    mail_sent = send_mail(subject, message, 'admin@squash_club.com', [reservation.user.email])

    return mail_sent
