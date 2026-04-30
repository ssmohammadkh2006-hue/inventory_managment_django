from django.db import models


class Product(models.Model):

    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('food', 'Food'),
        ('accessories', 'Accessories'),
    ]
    SUPPLIER_CHOICES = [
        ('amazon', 'Amazon'),
        ('alibaba', 'Alibaba'),
        ('local', 'Local Supplier'),
    ]

    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)
    quantity = models.PositiveIntegerField()  # المخزون الأساسي
    min_stock = models.PositiveIntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.CharField(max_length=50, choices=SUPPLIER_CHOICES, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    import_date = models.DateField(null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class Distributor(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    distributor_name = models.CharField(max_length=255)
    vehicle = models.CharField(max_length=100, null=True, blank=True)
    load = models.PositiveIntegerField(null=True, blank=True)
    quantity_taken = models.PositiveIntegerField()
    QUANTITY_TYPE_CHOICES = [
        ('boxes', 'Boxes'),
        ('units', 'Units'),
        ('kg', 'Kg'),
    ]
    quantity_type = models.CharField(max_length=20,choices=QUANTITY_TYPE_CHOICES,null=True,blank=True)
    quantity_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # خصم من المخزون عند الإضافة
        if self.pk is None:
            self.product.quantity -= self.quantity_taken
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.distributor_name
    
    
class Sale(models.Model):

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    buyer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # خصم من المخزون عند البيع
        if self.pk is None:
            self.product.quantity -= self.quantity
            self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.buyer_name} - {self.product.name}"