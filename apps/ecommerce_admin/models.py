from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone

# --------------------------------------------
# Category Model
# --------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# --------------------------------------------
# Status Model
# --------------------------------------------
class ProductStatus(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status

# --------------------------------------------
# Product Model
# --------------------------------------------
class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=1000, default="")
    image = models.ImageField(upload_to='products/', blank=True, null=True, default="")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], default=0)
    stock = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                 validators=[MinValueValidator(0.01)], default=0)
    purchase_date = models.DateField(default=timezone.now)
    order_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[A-Za-z0-9]{6,20}$', 'Order ID is missing or incorrect.')],
        default=""
    )
    status = models.ForeignKey(ProductStatus, on_delete=models.SET_NULL, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # Soft delete

    def is_editable(self):
        return self.status and self.status.status in ['not_shipped', 'processing']

    def __str__(self):
        return self.name

# --------------------------------------------
# Product Review Model
# --------------------------------------------
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    custom_label = models.CharField(max_length=100, blank=True, null=True, default="")
    review_text = models.TextField(max_length=500, blank=True, null=True, default="")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True, default=None
    )
    return_reason = models.CharField(max_length=100, blank=True, null=True, default="")
    return_comment = models.CharField(max_length=500, blank=True, null=True, default="")
    shipping_address = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"

# --------------------------------------------
# Product Relationship Mapping Models
# --------------------------------------------
class ProductCategoryMapping(models.Model):
    id = models.AutoField(primary_key=True)
    category_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductManufacturerMapping(models.Model):
    id = models.AutoField(primary_key=True)
    manufacturer_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductProductTagMapping(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_tag_id = models.IntegerField()

    class Meta:
        unique_together = ('product', 'product_tag_id')

class ProductPictureMapping(models.Model):
    id = models.AutoField(primary_key=True)
    picture_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductProductAttributeMapping(models.Model):
    id = models.AutoField(primary_key=True)
    product_attribute_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class ProductSpecificationAttributeMapping(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification_attribute_option_id = models.IntegerField()
