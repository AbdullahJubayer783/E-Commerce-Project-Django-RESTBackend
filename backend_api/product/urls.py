from django.contrib import admin
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet , CategoryViewSet , BrandViewSet , ProductVariantViewSet , ReviewViewSet , CommentViewSet

router = DefaultRouter()
router.register('brands',BrandViewSet)
router.register('category',CategoryViewSet)
router.register('product',ProductViewSet)
router.register('product-variant',ProductVariantViewSet)
router.register('review',ReviewViewSet)
router.register('comment',CommentViewSet)

urlpatterns = [
    path('',include(router.urls)),
]