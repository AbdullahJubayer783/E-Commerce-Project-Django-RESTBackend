from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Brand
class Brand(models.Model):
    logo = models.ImageField(upload_to='backend_api/product/media/brand_image')
    name = models.CharField(max_length=150)
    description = models.TextField(null=True,blank=True)
    def __str__(self):
        return f'Brand - {self.name}'

    class Meta:
        verbose_name_plural = "Brand"


# Category
class Category(MPTTModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=240)
    parent = TreeForeignKey('self',on_delete=models.PROTECT,null=True,blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'Category - {self.name}'

    class Meta:
        verbose_name_plural = "Category"


# Product Size
class Size(models.Model):
    size = models.CharField(max_length=6)



# Parent Class of Product and Product variants
class ProductAndVariantsCommonFields(models.Model):
    image = models.ImageField(upload_to='backend_api/product/media/product_image',null=True,blank=True)
    image_url = models.URLField(null=True,blank=True)
    size = models.ManyToManyField(Size)
    quantity = models.SmallIntegerField()
    selling_price = models.SmallIntegerField()
    discounted_price = models.SmallIntegerField()

    class Meta:
        abstract = True


# Product
class Product(ProductAndVariantsCommonFields):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=240)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product - {self.title}"
    
    class Meta:
        get_latest_by = ["-created_at"]
        verbose_name_plural = "Product"


# Product Varient
class ProductVariant(ProductAndVariantsCommonFields):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_variant',null=True,blank=True)

    def __str__(self):
        return f'{self.product.title} - {self.image_url}'