from django.conf import settings
from django.db import models
from users.models import User
Status_Choice=(
("process","processing"),
("shipment","shipped"),
("devivery", "delivered")

)
STATUS=(
("draft","Draft"),
("disabled","Disabled"),
("rejected", "Rejected"),
("in_review","In Review"),
("published","Published")
)
RATING=(
(1,"★☆☆☆☆"),
(2,"★★☆☆☆"),
(3, "★★★☆☆"),
(4,"★★★★☆"),
(5,"★★★★★")
)

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)

    product_id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.CASCADE)
    quality = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image=models.ImageField(blank=True, null=True)
    quantity=models.IntegerField()
    product_status=models.CharField(choices=STATUS,max_length=10,default="in_review")
    status=models.BooleanField(default=True)
    in_stock=models.BooleanField(default=True)
    feature=models.BooleanField(default=False)
    digital=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(null=True,blank=True)

    def getpercentage(self):
        new_price=((self.old_price - self.price) / self.old_price) * 100
        return new_price


    def __str__(self):
        return self.product_name

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    view_type = models.CharField(max_length=50, default='default_view')  # Set default value here

    def __str__(self):
        return f'Image for {self.product.product_name}'

class CartOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    paid_status=models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_type = models.CharField(max_length=50, default='deliver')
    payment_option = models.CharField(max_length=50, default='COD')
    delivery_address = models.CharField(max_length=100, default=None)
    township = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)
    phone_number = models.CharField(max_length=50, default=None)
    email = models.EmailField(default=None)

    class Meta:
        verbose_name_plural='Cart Order'



class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    item = models.CharField(max_length=300)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural='Cart OrderItems'



# class Order(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     quantity = models.PositiveIntegerField(default=1)  # Number of units ordered
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Total cost

#     def save(self, *args, **kwargs):
#         # Update total_amount based on product price and quantity
#         if self.total_amount is None:
#             self.total_amount = self.product.price * self.quantity
#         super().save(*args, **kwargs)
#     def __str__(self):
#         return f'Order {self.order_id} by {self.user.username}'

# class Payment(models.Model):
#     method = models.CharField(max_length=50)
#     payment_id = models.AutoField(primary_key=True)
#     date = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     transaction_id = models.CharField(max_length=255, unique=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50)
#     address = models.CharField(max_length=255, blank=True, null=True)  # Directly use the address field
#     phone_number = models.CharField(max_length=15, blank=True, null=True)  # Directly use the phone number field
#     def __str__(self):
#         return f'Payment {self.payment_id} for Order {self.order.order_id}'

class ProductReview(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    review_id = models.AutoField(primary_key=True)
    review=models.TextField()


    rating = models.IntegerField(choices=RATING,default=None)
    review_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='ProductReview'
    def __str__(self):
        return self.product.product_name if self.product else 'No Product'

    def get_rating(self):
        return self.rating

class wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='Wishlist'

    def __str__(self):
        return self.product.product_name
class UAddress(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    address=models.CharField(max_length=300,null=True)
    status=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='address'
