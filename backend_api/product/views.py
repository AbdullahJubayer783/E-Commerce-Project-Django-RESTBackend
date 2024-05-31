from rest_framework import viewsets
# from requests import Response 
from rest_framework.response import Response
from .models import Brand , Category , Product , ProductVariant
from .serializers import BrandSerializers , CategorySerializers , ProductSerializers , ProductVariatSerializers
from rest_framework import filters , status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def create(self, request, *args, **kwargs):
        product_variant_data = request.data.pop('product_variant', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        if product_variant_data:
            for variant_data in product_variant_data:
                variant_data['product_variant'] = product.id  # Set the product id
                variant_serializer = ProductVariatSerializers(data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variant_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProductvariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariatSerializers


class ParentCategoryFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        child_id = request.query_params.get('child')
        if child_id:
            queryobj = Category.objects.get(id=child_id)
            newobj = []

            while(queryobj!=None):
                newobj.append(queryobj)
                queryobj=queryobj.parent
            
            newobj = newobj[::-1]
            print('New OBJECT--->',newobj)
            return newobj
        return queryset
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    filter_backends = [ParentCategoryFilter]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers
