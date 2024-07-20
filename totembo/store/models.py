from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Category')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Image')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='subcategory', verbose_name='Category')

    def get_absolute_url(self):
        return reverse('category_list', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Name product')
    price = models.FloatField(verbose_name='Price')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    quantity = models.IntegerField(default=0, verbose_name='Quantity of product')
    description = RichTextField(default="Description will be soon", verbose_name='Description')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Siz in mm')
    colour = models.CharField(max_length=100, choices=[
        ('GOLD', 'gold'),
        ('SILVER', 'silver'),
        ('BLACK', 'black')
    ], verbose_name='Colour')

    def __str__(self):
        return self.title

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return "https://t4.ftcdn.net/jpg/07/91/22/59/240_F_791225927_caRPPH99D6D1iFonkCRmCGzkJPf36QDw.jpg"
        else:
            return "https://t4.ftcdn.net/jpg/07/91/22/59/240_F_791225927_caRPPH99D6D1iFonkCRmCGzkJPf36QDw.jpg"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


class Gallery(models.Model):
    image = models.ImageField(upload_to='products', verbose_name='Image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Review(models.Model):
    text = models.TextField(verbose_name='text')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.text[:20]


class FavouriteProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='USER')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')

    def __str__(self):
        return f"{self.user} - {self.product.title}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250)
    email = models.EmailField()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    shipping = models.BooleanField(default=True)

    def __str__(self):
        return str(self.pk)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
