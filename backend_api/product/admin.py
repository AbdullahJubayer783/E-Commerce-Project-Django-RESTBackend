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
    readonly_fields = ['discount_percent', 'product_code']
    prepopulated_fields = {"slug": ("title",)}

    def discount_percent(self, obj):
        return obj.discount_percent

    def product_code(self, obj):
        return obj.product_code


class ProductVarientAdmin(nested_admin.NestedModelAdmin):
    inlines = [ProductVarientImageInline]
    list_display = ['product','id', 'quantity', 'selling_price', 'discounted_price', 'discount_percent']
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