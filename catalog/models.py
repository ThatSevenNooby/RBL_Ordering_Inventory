from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default='Available') # e.g., Available, Out of Stock
    quantity = models.IntegerField(default=0)
    image_path = models.ImageField(upload_to='products/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Foreign Keys
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name