from rest_framework import viewsets, filters, pagination, status
from rest_framework.response import Response
from .models import Product, ProductVariant, Brand, Category, Review, Comment, ProductImage
from .serializers import ProductSerializers, ProductVariantSerializers, BrandSerializers, CategorySerializers, ReviewSerializers, CommentSerializer, ProductImageSerializer

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

    # def create(self, request, *args, **kwargs):
    #     product_variant_data = request.data.pop('product_variant', None)
    #     product_images_data = request.data.pop('images', None)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     product = serializer.save()

    #     if product_variant_data:
    #         for variant_data in product_variant_data:
    #             variant_data['product'] = product.id  # Set the product id
    #             variant_serializer = ProductVariantSerializers(data=variant_data)
    #             variant_serializer.is_valid(raise_exception=True)
    #             variant_serializer.save()

    #     if product_images_data:
    #         for image_data in product_images_data:
    #             image_data['products'] = product.id  # Set the product id
    #             image_serializer = ProductImageSerializer(data=image_data)
    #             image_serializer.is_valid(raise_exception=True)
    #             image_serializer.save()

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializers

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

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

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers

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