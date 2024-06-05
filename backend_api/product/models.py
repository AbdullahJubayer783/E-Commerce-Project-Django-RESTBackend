from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from django.contrib.auth.models import User
from backend_api.account.models import User

# Brand
class Brand(models.Model):
    logo = models.ImageField(upload_to='backend_api/product/media/brand_image')
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f'Brand - {self.name}'

    class Meta:
        verbose_name_plural = "Brand"


# Category
class Category(MPTTModel):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=240)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'Category - {self.name}'

    class Meta:
        verbose_name_plural = "Category"


# Product Size
class Size(models.Model):
    size = models.CharField(max_length=6)

    def __str__(self):
        return self.size


# Parent Class of Product and Product variants
class ProductAndVariantsCommonFields(models.Model):
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
    brand = models.ForeignKey(Brand,related_name='products', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product - {self.title}"

    class Meta:
        get_latest_by = ["-created_at"]
        verbose_name_plural = "Product"

    @property
    def discount_percent(self):
        return round(abs(((self.discounted_price / self.selling_price) * 100) - 100), 2)


# Product Variant
class ProductVariant(ProductAndVariantsCommonFields):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variant', null=True, blank=True)

    def __str__(self):
        return f'{self.product.title} - {self.id}'

    @property
    def discount_percent(self):
        return round(abs(((self.discounted_price / self.selling_price) * 100) - 100), 2)




# Multiple Image Model
class ProductImage(models.Model):
    image = models.ImageField(upload_to='backend_api/product/media/product_image', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    product = models.ForeignKey(Product,related_name='product_images', on_delete=models.CASCADE, null=True, blank=True)
    product_variant = models.ForeignKey(ProductVariant,related_name='product_varient_images', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.product.title if self.product else self.product_variant.product.title} - {self.image_url}'





# Product Review
STARCHOICE = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐')
]

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField()
    rating = models.CharField(choices=STARCHOICE, max_length=7)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Reviewer: {self.reviewer.first_name}| Doctor: {self.product.title}"


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.user.first_name}'