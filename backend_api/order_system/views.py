from rest_framework import generics
from .models import Cart
from .serializers import CartCreateSerializer , CartListSerializer
from rest_framework import viewsets
from .models import Order, Address, Coupon
from .serializers import OrderCreateSerializer,OrderGetSerializer, AddressSerializer, CouponSerializer
from rest_framework.permissions import IsAuthenticated

# Cart
# -----------------------------------------------------------
class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartCreateSerializer

class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartListSerializer
# -----------------------------------------------------------

# Order
# -----------------------------------------------------------
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
# -----------------------------------------------------------