from rest_framework import viewsets, filters, pagination, status
from rest_framework.response import Response
from .models import Product, ProductVariant, Brand, Category, Review, Comment, ProductImage
from .serializers import ProductSerializers, ProductVariantSerializers, BrandSerializers, CategorySerializers, ReviewSerializers, CommentSerializer, ProductImageSerializer
from backend_api.renderers import UserRenderer


class ProductPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'slug', 'description', 'category__name', 'brand__name', 'size__size', 'selling_price', 'discounted_price']
    pagination_class = ProductPagination
    renderer_classes = [UserRenderer]

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializers
    renderer_classes = [UserRenderer]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    renderer_classes = [UserRenderer]

class ParentCategoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        child_id = request.query_params.get('child')
        if child_id:
            queryobj = Category.objects.get(id=child_id)
            newobj = []

            while queryobj is not None:
                newobj.append(queryobj)
                queryobj = queryobj.parent

            newobj = newobj[::-1]
            print('New OBJECT--->', newobj)
            return newobj
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = [ParentCategoryFilter]
    renderer_classes = [UserRenderer]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
    renderer_classes = [UserRenderer]

class ReviewsForSpecificProduct(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_id = request.query_params.get('product_id')
        if product_id:
            return queryset.filter(product=product_id)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    filter_backends = [ReviewsForSpecificProduct]
    renderer_classes = [UserRenderer]

class CommentForSpecificProduct(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        product_id = request.query_params.get('product_id')
        if product_id:
            return queryset.filter(product=product_id)
        return queryset

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [CommentForSpecificProduct]
    renderer_classes = [UserRenderer]