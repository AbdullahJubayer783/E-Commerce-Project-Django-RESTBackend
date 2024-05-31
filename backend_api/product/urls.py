from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet , CategoryViewSet , BrandViewSet , ProductvariantViewSet

router = DefaultRouter()
router.register('brands',BrandViewSet)
router.register('category',CategoryViewSet)
router.register('product',ProductViewSet)
router.register('product-variant',ProductvariantViewSet)

urlpatterns = [
    path('',include(router.urls)),
]