from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    image_path = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)