from celery import shared_task
from django.core.mail import send_mail
from sms import send_sms


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


@shared_task
def send_sms_notification(notification_id):
    """Zadanie wysyłające powiadomienie sms, gdy zwolni się któryś z kortów, w zajętym terminie"""
    from courts.models import Notification
    notification = Notification.objects.get(pk=notification_id)
    message = f"Witaj, {notification.user.username}!\n Informujemy, że zwolnił się kort do {notification.category}a " \
              f"w terminie {notification.date}. Jeśli nadal chcesz zagrać, wejdź na naszą stronę i zrób rezerwację. \n" \
              f"Pozdrowienia, SquashClub"
    originator = "+48600600600"
    recipients = [f"+48{notification.user.profile.phone_number}"]
    sms_sent = send_sms(message, originator, recipients, fail_silently=False)

    return sms_sent
