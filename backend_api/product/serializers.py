from rest_framework import serializers
from .models import Product, ProductVariant, ProductImage, Brand, Category, Review, Comment


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    # products = ProductSerializers(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

# Product Varient Section
class ProductVarientImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url']


class ProductVariantSerializers(serializers.ModelSerializer):
    product_varient_images = ProductVarientImageSerializer(many=True, required=False)

    class Meta:
        model = ProductVariant
        fields = ['id', 'size', 'quantity', 'selling_price', 'discounted_price', 'discount_percent', 'product_varient_images']
        depth = 1

    def create(self, validated_data):
        product_images_data = validated_data.pop('images', None)
        product = Product.objects.create(**validated_data)

        if product_images_data:
            for image_data in product_images_data:
                ProductImage.objects.create(products=product, **image_data)

        return product


# Product Section
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url']

    
#-----------------------------------


class ProductSerializers(serializers.ModelSerializer):
    product_variant = ProductVariantSerializers(many=True)
    product_images = ProductImageSerializer(many=True)
    category = CategorySerializers(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug','quantity', 'selling_price', 'discounted_price', 'discount_percent', 'brand', 'category','category_id', 'product_variant', 'product_images']

    # def __init__(self,*args, **kwargs):
    #     super(ProductSerializers,self).__init__(*args, **kwargs)
    #     self.Meta.depth = 1

    def create(self, validated_data):
        product_variant_data = validated_data.pop('product_variant')
        product_images_data = validated_data.pop('product_images')
        
        category = validated_data.pop('category_id')
        brand = validated_data.pop('brand', None)
        

        product = Product.objects.create(category=category, brand=brand, **validated_data)
        
        # Create product variants
        for variant_data in product_variant_data:
            images_data = variant_data.pop('product_varient_images')
            variant = ProductVariant.objects.create(product=product, **variant_data)
            
            # Create product variant images
            for image_data in images_data:
                ProductImage.objects.create(product_variant=variant, **image_data)

        # Create product images
        for image_data in product_images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        return product

    def validate_category(self, value):
        if not Category.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Category does not exist.")
        return value

    def validate_brand(self, value):
        if value and not Brand.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Brand does not exist.")
        return value




#-----------------------------------





class ReviewSerializers(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(many=False)

    class Meta:
        model = Review
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source="user.email")

    class Meta:
        model = Comment
        fields = ['id', 'user_email', 'product_id', 'parent', 'body', 'created_on']
        depth = 1


