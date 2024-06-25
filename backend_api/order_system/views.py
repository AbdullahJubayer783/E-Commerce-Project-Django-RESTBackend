from rest_framework import generics
from .models import Cart
from .serializers import CartCreateSerializer , CartListSerializer
from rest_framework import viewsets
from .models import Order, Address, Coupon
from .serializers import OrderCreateSerializer,OrderGetSerializer, AddressSerializer, CouponSerializer
from rest_framework.permissions import IsAuthenticated
from backend_api.renderers import UserRenderer
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from .models import Payment
from backend_api.order_system.serializers import OrderGetSerializer , PaymentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

# Cart
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

# Order
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAuthenticated]


class OrderCreateViewSet(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)

        if order.payment_method != 'Cash on Delivery':
            # Initiate payment
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
                'cus_add1': 'Billing Address',
                'cus_city': 'Narayanganj',
                'cus_postcode': '1430',
                'cus_country': 'Bangladesh',
                'cus_phone': '017373267',
                'shipping_method': order.shipping_method,
                'product_name': order.product.name if order.product else 'N/A',
                'product_category': 'General',
                'product_profile': 'general',
                'ship_name': order.user.username,  # Add ship_name here
                'ship_add1': 'dfsdfds',
                'ship_city': 'sdfds',
                'ship_postcode': 'slfjee',
                'ship_country': 'Bangladesh',
            }

            response = requests.post(payment_url, data=post_data)
            response_data = response.json()
            print("Responst---",response_data)
            if response_data['status'] == 'SUCCESS':
                headers = self.get_success_headers(serializer.data)
                return Response({'order': serializer.data, 'gateway_url': response_data['GatewayPageURL']}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                order.delete()  # If payment initiation fails, delete the created order
                return Response({'error': response_data['failedreason']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            headers = self.get_success_headers(serializer.data)
            return Response({'order': serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
    
class OrderListViewSet(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
class OrderGetViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)



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
    return Response({'error': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def payment_cancel(request):
    return Response({'message': 'Payment cancelled'}, status=status.HTTP_200_OK)
