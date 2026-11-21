from django.conf import settings
from django.db import models
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Preparing", "Preparing"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    PAYMENT_CHOICES = [("COD", "Cash on Delivery")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="food_orders")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=12)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="COD")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Pending")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} – {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} × {self.product_name}"
