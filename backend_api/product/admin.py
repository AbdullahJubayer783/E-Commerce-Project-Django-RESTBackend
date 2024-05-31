from django.contrib import admin
from .models import Brand , Category , Size , Product , ProductVariant

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fk_name = 'product'  # Specify the correct ForeignKey

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ('title', 'category', 'brand', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_url', 'quantity', 'selling_price', 'discounted_price')


admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Size)
