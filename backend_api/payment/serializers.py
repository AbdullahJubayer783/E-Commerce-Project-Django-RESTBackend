from rest_framework import serializers
from .models import Payment
from backend_api.order_system.serializers import OrderGetSerializer

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


