from django.contrib import admin
from django.contrib import admin
from .models import (
    Category,
    ProductStatus,
    Product,
    ProductReview,
    ProductCategoryMapping,
    ProductManufacturerMapping,
    ProductProductTagMapping,
    ProductPictureMapping,
    ProductProductAttributeMapping,
    ProductSpecificationAttributeMapping
)

# --------------------------------------------
# Category Admin
# --------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# --------------------------------------------
# Product Status Admin
# --------------------------------------------
@admin.register(ProductStatus)
class ProductStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
    search_fields = ('status',)


# --------------------------------------------
# Product Admin
# --------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'owner', 'category', 'price',
        'stock', 'status', 'purchase_date', 'order_id', 'deleted_at'
    )
    list_filter = ('status', 'category', 'purchase_date')
    search_fields = ('name', 'description', 'order_id', 'owner__username')
    readonly_fields = ('deleted_at',)


# --------------------------------------------
# Product Review Admin
# --------------------------------------------
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'user', 'rating', 'custom_label',
        'return_reason', 'return_comment'
    )
    list_filter = ('rating', 'product')
    search_fields = ('product__name', 'user__username', 'review_text')


# --------------------------------------------
# ProductCategoryMapping Admin
# --------------------------------------------
@admin.register(ProductCategoryMapping)
class ProductCategoryMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'category_id')


# --------------------------------------------
# ProductManufacturerMapping Admin
# --------------------------------------------
@admin.register(ProductManufacturerMapping)
class ProductManufacturerMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'manufacturer_id')


# --------------------------------------------
# ProductProductTagMapping Admin
# --------------------------------------------
@admin.register(ProductProductTagMapping)
class ProductProductTagMappingAdmin(admin.ModelAdmin):
    list_display = ('product', 'product_tag_id')
    list_filter = ('product_tag_id',)
    search_fields = ('product__name',)


# --------------------------------------------
# ProductPictureMapping Admin
# --------------------------------------------
@admin.register(ProductPictureMapping)
class ProductPictureMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'picture_id')


# --------------------------------------------
# ProductProductAttributeMapping Admin
# --------------------------------------------
@admin.register(ProductProductAttributeMapping)
class ProductProductAttributeMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'product_attribute_id')


# --------------------------------------------
# ProductSpecificationAttributeMapping Admin
# --------------------------------------------
@admin.register(ProductSpecificationAttributeMapping)
class ProductSpecificationAttributeMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'specification_attribute_option_id')
