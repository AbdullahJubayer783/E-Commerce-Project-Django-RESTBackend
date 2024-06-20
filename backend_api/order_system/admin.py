from django.contrib import admin
from .models import Cart

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'product_variant', 'quantity')
    list_filter = ('user', 'product', 'product_variant')
    search_fields = ('user__username', 'product__name', 'product_variant__name')

admin.site.register(Cart, CartAdmin)



from django.contrib import admin
from .models import Order, Address, Coupon

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'city', 'state', 'postal_code', 'country', 'address_type']
    search_fields = ['user__username', 'street_address', 'city', 'state', 'postal_code', 'country']
    list_filter = ['address_type', 'city', 'state', 'country']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'active', 'created_at', 'expires_at']
    search_fields = ['code']
    list_filter = ['discount_type', 'active', 'created_at', 'expires_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'product_variant', 'quantity', 'created_at', 'updated_at', 'status', 'coupon', 'shipping_method', 'payment_method', 'tracking_number', 'total_price']
    search_fields = ['user__username', 'product__title', 'product_variant__product__title', 'tracking_number']
    list_filter = ['status', 'shipping_method', 'payment_method', 'created_at', 'updated_at']
    readonly_fields = ['total_price', 'order_code' , 'apply_coupon_price', 'shipping_charge', 'product_price', 'subtotal_price']

    def order_code(self, obj):
        return obj.order_code
    

    def total_price(self, obj):
        return obj.total_price

    def apply_coupon_price(self, obj):
        return obj.apply_coupon_price

    def shipping_charge(self, obj):
        return obj.shipping_charge

    def product_price(self, obj):
        return obj.product_price

    def subtotal_price(self, obj):
        return obj.subtotal_price

admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)
