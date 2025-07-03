from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from PIL import Image
#change forms register django
#category
#Congthuc
class Recipe(models.Model):
    # Các lựa chọn phân loại công thức
    TYPE_CHOICES = [
        ('vegetarian', 'Món chay'),
        ('meat', 'Món mặn'),
        ('dessert', 'Món tráng miệng'),
    ]
    
    name = models.CharField(max_length=200)  # Tên món ăn
    description = models.TextField(null=True, blank=True)  # Mô tả món ăn
    ingredients = models.TextField()  # Nguyên liệu
    steps = models.TextField()  # Các bước thực hiện
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)  # Hình ảnh món ăn
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='meat')  # Loại món ăn

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            # Resize ảnh nếu kích thước quá lớn
            if img.width > 300 or img.height > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)
    def __str__(self):
        return self.name
    
class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='detail_step')
    description = models.TextField()  # Nội dung của bước (đã bao gồm thông tin bước như "Bước 1:")
    image = models.ImageField(upload_to='steps/', null=True, blank=True)  # Hình minh họa

    def __str__(self):
        # Hiển thị phần đầu của nội dung bước để phân biệt trong Django Admin
        return f"Bước: {self.description[:50]} của {self.recipe.name}"

class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True,blank=True)
    is_sub =  models.BooleanField(default=False)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,unique=True)
    def __str__(self):
        return self.name
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class Product(models.Model):
    category = models.ManyToManyField(Category,related_name='product')
    name = models.CharField(max_length=200, null=True)  # Tên sản phẩm (ví dụ: Rau cải, Cà rốt)
    price = models.DecimalField(max_digits=10, decimal_places=3)  # Giá sản phẩm
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    quantity = models.IntegerField(default=0)  # Số lượng trong kho
    unit = models.CharField(max_length=50, default='kg')  # Đơn vị tính (ví dụ: kg, quả, bó)
    detail = models.TextField(null=True,blank=True)

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
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="orders")
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank', 'Chuyển khoản ngân hàng'),
        ('momo', 'Momo'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True
    )
    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.items.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_items")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="items")
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="addresses")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, related_name="shipping_addresses")
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)