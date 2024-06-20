from django.db import models
from backend_api.account.models import User
from backend_api.product.models import Product , ProductVariant 
from django.utils.crypto import get_random_string


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_carts')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='products',null=True,blank=True)
    product_variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE, related_name='variants',null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    size = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self) -> str:
        return f"User - {self.user.name} Product - {self.product} Product Variant - {self.product_variant}"
    
    class Meta:
        verbose_name_plural = 'Cart'
        
    @property
    def subtotal_cost(self):
        if self.product:
            return self.product.discounted_price * self.quantity
        if self.product_variant:
            return self.product_variant.discounted_price * self.quantity


# Shipping Address of User

STATE_CHOICES = (
    ('Dhaka','Dhaka'),
    ('Chittagong','Chittagong'),
    ('Khulna','Khulna'),
    ('Barishal','Barishal'),
    ('Rajsahi','Rajsahi'),
    ('Shylet','Shylet'),
    ('Jashor','Jashor'),
    ('Bramonbaria','Bramonbaria')
)

ADDRESS_TYPE = (
    ('Shipping', 'Shipping'),
    ('Billing', 'Billing')
)
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,choices=STATE_CHOICES)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPE , default='Shipping')

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}, {self.postal_code}, {self.country}"


# order and order list of user

# Coupon

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=[
        ('percent', 'Percent'),
        ('amount', 'Amount')
    ])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.code

# Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    ], default='Pending')
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_orders', on_delete=models.SET_NULL, null=True, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_orders', on_delete=models.SET_NULL, null=True, blank=True)
    shipping_method = models.CharField(max_length=50, choices=[
        ('Inside Dhaka', 'Inside Dhaka'),
        ('Outside Dhaka', 'Outside Dhaka'),
        ('Dhaka Sub Area', 'Dhaka Sub Area')
    ], default='Inside Dhaka')
    payment_method = models.CharField(max_length=50, choices=[
        ('Credit Card', 'Credit Card'),
        ('Bkash', 'Bkash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash on Delivery', 'Cash on Delivery')
    ])
    tracking_number = models.CharField(max_length=100, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Order'

    def __str__(self):
        return f"Order {self.id} by {self.user.name}"
    
    @property
    def order_code(self):
        code = '#' + get_random_string(10).upper()
        return code 

    @property
    def product_price(self):
        if self.product_variant:
            return self.product_variant.discounted_price
        elif self.product:
            return self.product.discounted_price

    @property
    def subtotal_price(self):
        return self.quantity * self.product_price

    @property
    def apply_coupon_price(self):
        if self.coupon and self.coupon.active:
            if self.coupon.discount_type == 'percent':
                discount_amount = (self.subtotal_price * self.coupon.discount_value) / 100
            elif self.coupon.discount_type == 'amount':
                discount_amount = self.coupon.discount_value
            final_price = max(self.subtotal_price - discount_amount, 0)
        else:
            final_price = self.subtotal_price
        return final_price

    @property
    def shipping_charge(self):
        if self.shipping_method == 'Inside Dhaka':
            return 50
        elif self.shipping_method == 'Outside Dhaka':
            return 110
        elif self.shipping_method == 'Dhaka Sub Area':
            return 90
        return 0

    @property
    def total_price(self):
        vat_tax = 5  # 5% VAT
        subtotal_with_discount_and_shipping = self.apply_coupon_price + self.shipping_charge
        return subtotal_with_discount_and_shipping + (subtotal_with_discount_and_shipping * vat_tax / 100)