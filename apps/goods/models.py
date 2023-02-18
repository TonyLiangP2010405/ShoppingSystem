from datetime import datetime
from django.db import models


# Create your models here.


class ProductsCategory(models.Model):
    category_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.category_id) + self.name

    class Meta:
        verbose_name = 'products category'
        verbose_name_plural = 'product categories'
        db_table = 'd_productsCategory'


class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ProductsCategory, on_delete=models.DO_NOTHING)
    main_image = models.ImageField(upload_to='productImage')
    price = models.DecimalField(max_digits=32, decimal_places=8)
    property1 = models.CharField(max_length=5000)
    property2 = models.CharField(max_length=5000)
    property3 = models.CharField(max_length=5000)
    property4 = models.CharField(max_length=5000)
    property5 = models.CharField(max_length=5000)
    property6 = models.CharField(max_length=5000)
    sale_number = models.IntegerField()
    sale_amount = models.IntegerField()
    rating_choice = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    customer_rating = models.IntegerField(choices=rating_choice)
    review = models.TextField()
    temporary_status_choice = ((0, "out-of-stock"), (1, "normal"))
    temporary_status = models.IntegerField(choices=temporary_status_choice)
    photo1 = models.ImageField(upload_to="productImage", blank=True)
    photo2 = models.ImageField(upload_to="productImage", blank=True)
    photo3 = models.ImageField(upload_to="productImage", blank=True)
    photo4 = models.ImageField(upload_to="productImage", blank=True)
    createDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id) + self.name

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = 'd_product'
