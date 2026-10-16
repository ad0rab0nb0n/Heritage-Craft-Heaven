from django.contrib import admin
from .models import Product, Category, ProductImage, CartOrder,CartOrderItems, ProductReview, Manufacturer,wishlist,UAddress

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4  # Allows up to 4 images to be added by default

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'category', 'manufacturer', 'quality','user','product_status','feature')
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'delivery_address', 'payment_option', 'order_date', 'total_price')

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'price','quantity','item','total')


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'user', 'product', 'rating',)
class wishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address','status')



@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductImage)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(wishlist,wishlistAdmin)
admin.site.register(UAddress,AddressAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
