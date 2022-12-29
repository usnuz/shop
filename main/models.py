from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User, BillingDetails


class SubCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Promo(models.Model):
    code = models.CharField(max_length=255, unique=True)
    percent = models.IntegerField(validators=[MaxValueValidator(50), MinValueValidator(10)])
    usr = models.ManyToManyField(User, related_name='promos')
    product = models.ManyToManyField('Product', related_name='promos')

    def __str__(self):
        return self.code


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductImg(models.Model):
    img = models.ImageField(upload_to="product/")


class Info(models.Model):
    key = models.CharField(max_length=255, null=True, blank=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.key


class Review(models.Model):
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    explain = models.CharField(max_length=255, blank=True, null=True)
    usr = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.rating)


class Characteristic(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    characteristics = models.ManyToManyField(Characteristic, blank=True)
    images = models.ManyToManyField(ProductImg, null=True, blank=True)
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    info = models.ManyToManyField(Info, null=True, blank=True)
    review = models.ManyToManyField(Review, blank=True)
    is_active = models.BooleanField(default=False)
    is_slider = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class WishList(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    usr = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    billing_detail = models.ForeignKey(BillingDetails, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.product.name
