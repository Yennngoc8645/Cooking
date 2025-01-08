from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)  # Tên sản phẩm (ví dụ: Rau cải, Cà rốt)
    price = models.DecimalField(max_digits=10, decimal_places=3)  # Giá sản phẩm
    category = models.CharField(
        max_length=50,
        choices=[('RAU', 'Rau'), ('CU', 'Củ'), ('QUA', 'Quả')],
        default='RAU'
    )  # Phân loại sản phẩm
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    quantity = models.IntegerField(default=0)  # Số lượng trong kho
    unit = models.CharField(max_length=50, default='kg')  # Đơn vị tính (ví dụ: kg, quả, bó)
    description = models.TextField(null=True, blank=True)  # Mô tả sản phẩm

    def __str__(self):
        return self.name
    @property
    def ImageProduct(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_items")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, related_name="addresses")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="shipping_addresses")
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=10, null=True)
