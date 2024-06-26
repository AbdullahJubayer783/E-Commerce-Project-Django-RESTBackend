from .views import CartListCreateView, CartDetailView , CartListView
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet, CouponViewSet, OrderCreateViewSet , OrderListViewSet , OrderGetViewSet , payment_success , payment_fail , payment_cancel

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')
router.register('coupons', CouponViewSet, basename='coupon')

urlpatterns = [
    path('cart-create/', CartListCreateView.as_view(), name='cart-list-create'),
    path('cart-list-read/', CartListView.as_view(), name='cart-list'),
    path('cart-read/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('', include(router.urls)),
    path('order-create/', OrderCreateViewSet.as_view(),name='order-create'),
    path('order-list/', OrderListViewSet.as_view(),name='order-list'),
    path('order-get/', OrderGetViewSet.as_view(),name='order-get'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-fail/', payment_fail, name='payment_fail'),
    path('payment-cancel/', payment_cancel, name='payment_cancel'),
]
