from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group, Permission

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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
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
    deleted_at = models.DateTimeField(null=True, blank=True)

    def is_editable(self):
        return self.status and self.status.status in ['not_shipped', 'processing']

    def __str__(self):
        return self.name

# --------------------------------------------
# Product Review Model
# --------------------------------------------
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
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
        return f"Review by {self.user} for {self.product.name}"

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

# --------------------------------------------
# Custom Admin Model
# --------------------------------------------
class AdminManager(BaseUserManager):
    def create_user(self, email, full_name, mobile, password=None):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), full_name=full_name, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, mobile, password):
        user = self.create_user(email, full_name, mobile, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Admin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    crn = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    profile_completed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(Group, related_name='custom_admin_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_admin_permissions', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'mobile']

    objects = AdminManager()

    def __str__(self):
        return self.full_name
