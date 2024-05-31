from rest_framework import serializers
from .models import Brand , Category , Product , ProductVariant

class ProductVariatSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    product_variant = ProductVariatSerializers(many=True,required=False)
    class Meta:
        model = Product
        fields = ['image','image_url','size','quantity','title','description','slug','selling_price','discounted_price','brand','category','product_variant']

    def create(self, validated_data):
        ProductVariant_data = validated_data.pop('product_variant', None)
        product = Product.objects.create(**validated_data)

        if ProductVariant_data:
            for variant_data in ProductVariant_data:
                # Create ProductVariant objects associated with the newly created Product
                ProductVariant.objects.create(ProductVariant=product, **variant_data)

        return product
