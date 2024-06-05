# from django.contrib import admin
# from .models import Brand , Category , Size , Product , ProductVariant , Review , Comment , ProductImage

# class ProductVariantInline(admin.TabularInline):
#     model = ProductVariant
#     fk_name = 'product'  # Specify the correct ForeignKey
    
# class ProductVariantInline(admin.TabularInline):
#     model = ProductVariant
#     fk_name = 'product'  # Specify the correct ForeignKey

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [ProductVariantInline]
#     list_display = ('title', 'category', 'brand', 'created_at', 'updated_at')
#     search_fields = ('title', 'description')
#     prepopulated_fields = {'slug': ('title',)}

# @admin.register(ProductVariant)
# class ProductVariantAdmin(admin.ModelAdmin):
#     list_display = ('product', 'image_url', 'quantity', 'selling_price', 'discounted_price')


# admin.site.register(Brand)
# admin.site.register(Category)
# admin.site.register(Size)
# admin.site.register(Review)
# admin.site.register(ProductImage)
# admin.site.register(Size)







# ChatGPT Code


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1
#     fk_name = 'product'

# class ProductVariantImageInline(nested_admin.NestedStackedInline):
#     model = ProductImage
#     extra = 1
#     fk_name = 'product_variant'

# class ProductVariantInline(nested_admin.NestedStackedInline):
#     model = ProductVariant
#     extra = 1
#     inlines = [ProductVariantImageInline]

# @admin.register(ProductVariant)
# class ProductVariantAdmin(nested_admin.NestedModelAdmin):
#     inlines = [ProductVariantImageInline]
#     list_display = ['product', 'quantity', 'selling_price', 'discounted_price', 'discount_percent']
#     search_fields = ['product__title']
#     list_filter = ['product']

# @admin.register(Product)
# class ProductAdmin(nested_admin.NestedModelAdmin):
#     inlines = [ProductImageInline, ProductVariantInline]
#     list_display = ['title', 'brand', 'category', 'selling_price', 'discounted_price', 'discount_percent']
#     search_fields = ['title', 'description', 'category__name', 'brand__name']
#     list_filter = ['brand', 'category']
#     prepopulated_fields = {"slug": ("title",)}

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ['image_url', 'product', 'product_variant']
#     search_fields = ['product__title', 'product_variant__product__title']
#     list_filter = ['product__title', 'product_variant__product__title']

#--------------------------------------------
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Brand, Category, Size, Product, ProductVariant, Review, Comment, ProductImage
import nested_admin



class ProductImageInline(nested_admin.NestedStackedInline):
    exclude = ('product_variant',)
    model = ProductImage
    extra = 1

class ProductVarientImageInline(nested_admin.NestedStackedInline):
    exclude = ('product',)
    model = ProductImage
    extra = 1

class ProductVariantInline(nested_admin.NestedStackedInline):
    model = ProductVariant
    extra = 1
    inlines = [ProductVarientImageInline]  

class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductVariantInline,ProductImageInline]
    list_display = ['title', 'brand', 'category', 'selling_price', 'discounted_price', 'discount_percent']
    search_fields = ['title', 'description', 'category__name', 'brand__name']
    list_filter = ['brand', 'category']
    prepopulated_fields = {"slug": ("title",)}

class ProductVarientAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductVarientImageInline]
    list_display = ['product', 'quantity', 'selling_price', 'discounted_price', 'discount_percent']
    search_fields = ['product__title']
    list_filter = ['product']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'product', 'product_variant']
    search_fields = ['product__title', 'product_variant__product__title']
    list_filter = ['product__title', 'product_variant__product__title']


admin.site.register(ProductVariant,ProductVarientAdmin)
admin.site.register(Product, ProductAdmin)

#--------------------------------------------

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'name'
    list_display = ['tree_actions', 'id', 'indented_title', 'related_products_count', 'related_products_cumulative_count']
    search_fields = ['name']
    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    search_fields = ['size']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'reviewer', 'rating', 'created_on']
    search_fields = ['product__title', 'reviewer__username']
    list_filter = ['rating', 'created_on']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'body', 'created_on', 'active']
    search_fields = ['product__title', 'user__username', 'body']
    list_filter = ['active', 'created_on']
# ChatGPT Code