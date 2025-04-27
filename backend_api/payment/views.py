import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Payment
from .serializers import PaymentSerializer

@api_view(['POST'])
def initiate_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment_url = settings.SSL_COMMERZ_API_URL

    post_data = {
        'store_id': settings.SSL_COMMERZ_STORE_ID,
        'store_passwd': settings.SSL_COMMERZ_STORE_PASSWORD,
        'total_amount': order.total_price,
        'currency': 'BDT',
        'tran_id': f'{order.id}{order.user.id}',  # Unique transaction ID
        'success_url': request.build_absolute_uri('/api/payment-success/'),
        'fail_url': request.build_absolute_uri('/api/payment-fail/'),
        'cancel_url': request.build_absolute_uri('/api/payment-cancel/'),
        'cus_name': order.user.name,
        'cus_email': order.user.email,
        'cus_add1': order.billing_address.address_line,
        'cus_city': order.billing_address.city,
        'cus_postcode': order.billing_address.postcode,
        'cus_country': 'Bangladesh',
        'cus_phone': order.user.phone_number,
        'shipping_method': order.shipping_method,
        'product_name': order.product.name if order.product else 'N/A',
        'product_category': 'General',
        'product_profile': 'general',
    }

    response = requests.post(payment_url, data=post_data)
    response_data = response.json()

    if response_data['status'] == 'SUCCESS':
        return Response({'gateway_url': response_data['GatewayPageURL']})
    else:
        return Response({'error': response_data['failedreason']}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_success(request):
    transaction_id = request.data.get('tran_id')
    order_id = transaction_id[:-len(str(request.user.id))]
    order = get_object_or_404(Order, id=order_id)

    if request.data.get('status') == 'VALID':
        order.status = 'Processing'
        order.save()
        
        payment = Payment.objects.create(
            order=order,
            transaction_id=transaction_id,
            amount=order.total_price,
            currency='BDT',
            status='Successful'
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
    else:
        return Response({'error': 'Invalid payment status'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_fail(request):
    # Handle failed payment
    return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_cancel(request):
    # Handle cancelled payment
    return Response({'message': 'Payment cancelled'}, status=status.HTTP_200_OK)
