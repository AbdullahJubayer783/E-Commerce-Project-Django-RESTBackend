from rest_framework import serializers
from .models import Cart , Order, Address, Coupon

# Cart 

class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_variant', 'quantity']

    def validate(self, data):
        product = data.get('product')
        product_variant = data.get('product_variant')

        if not product and not product_variant:
            raise serializers.ValidationError("Either product or product_variant must be provided.")
        
        if product and product_variant:
            raise serializers.ValidationError("Only one of product or product_variant should be provided, not both.")

        return data
    

class CartListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_variant', 'quantity']
        depth = 3

# ------------------------------------------------------------------------


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street_address', 'city', 'state', 'postal_code', 'country', 'address_type']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'active', 'created_at', 'expires_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    apply_coupon_price = serializers.ReadOnlyField()
    shipping_charge = serializers.ReadOnlyField()
    product_price = serializers.ReadOnlyField()
    subtotal_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product', 'product_variant', 'quantity', 'created_at', 'updated_at', 'status', 'coupon', 
            'shipping_address', 'billing_address', 'shipping_method', 'payment_method', 'tracking_number', 
            'total_price', 'apply_coupon_price', 'shipping_charge', 'product_price', 'subtotal_price','order_code'
        ]
    def create(self, validated_data):
        order = super().create(validated_data)
        order.status = 'Pending'
        order.save()
        return order

class OrderGetSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    apply_coupon_price = serializers.ReadOnlyField()
    shipping_charge = serializers.ReadOnlyField()
    product_price = serializers.ReadOnlyField()
    subtotal_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'product', 'product_variant', 'quantity', 'created_at', 'updated_at', 'status', 'coupon', 
            'shipping_address', 'billing_address', 'shipping_method', 'payment_method', 'tracking_number', 
            'total_price', 'apply_coupon_price', 'shipping_charge', 'product_price', 'subtotal_price','order_code'
        ]
        depth = 3


from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'