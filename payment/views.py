from django.shortcuts import render, get_object_or_404, redirect
import braintree
from django.views import View

from courts.models import Reservation
from squash_club import settings

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class PaymentProcessView(View):
    def get(self, request):
        reservation_id = request.session.get('reservation_id')
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        client_token = gateway.client_token.generate()
        return render(request, 'payment_process.html', {'client_token': client_token, 'reservation': reservation})

    def post(self, request):
        reservation_id = request.session.get('reservation_id')
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        nonce = request.POST.get('payment_method_nonce', None)
        result = gateway.transaction.sale({
            'amount': f'{reservation.price}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if result.is_success:
            reservation.paid = True
            reservation.braintree_id = result.transaction.id
            reservation.save()
            return redirect('payment_done')
        else:
            return redirect('payment_cancelled')


def payment_done(request):
    return render(request, 'payment_done.html')


def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')
