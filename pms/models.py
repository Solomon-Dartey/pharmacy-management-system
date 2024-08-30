from django.db import models
from django.utils import timezone
from datetime import timedelta

from pharmarcy import settings

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()
    email = models.EmailField()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PackagingType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Drug(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quantity = models.PositiveIntegerField()  # Initial quantity for new drug entry
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    generic_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    BATCH_CHOICES = (
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
    )
    batch = models.CharField(max_length=50, choices=BATCH_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    packaging_type = models.ForeignKey(PackagingType, on_delete=models.CASCADE)
    strength = models.CharField(max_length=20)

    def is_expiring_soon(self):
        return self.expiry_date <= timezone.now().date() + timedelta(days=30)

    def __str__(self):
        return f"{self.name} (Batch: {self.batch})"

class Stock(models.Model):
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.drug.name} - {self.quantity} units"



class Alert(models.Model):
    LOW_STOCK = 'low_stock'
    EXPIRY_WARNING = 'expiry_warning'
    OTHER = 'other'

    ALERT_TYPE_CHOICES = [
        (LOW_STOCK, 'Low Stock'),
        (EXPIRY_WARNING, 'Expiry Warning'),
        (OTHER, 'Other'),
    ]

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    alert_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES, default='Alert')
    
    def __str__(self):
        return self.message


# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.contrib.auth import get_user_model
def generate_staff_id():
    prefix = "PSM00"
    while True:
        unique_number = random.randint(1000, 9999)
        staff_id = f"{prefix}{unique_number}"
        if not CustomUser.objects.filter(staff_id=staff_id).exists():
            return staff_id

class CustomUser(AbstractUser):
    coices = (
        ('Manager', 'Manager'),
        ('Pharmacist', 'Pharmacist')
    )
    middle_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    role = models.CharField(max_length=50,choices=coices)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = generate_staff_id()
        super(CustomUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

# New models for cart and sale
class Cart(models.Model):
    pharmacist = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Sale(models.Model):
    pharmacist = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sale_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=20, unique=True, blank=True, null=True)  # New field

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = generate_receipt_number()
        super(Sale, self).save(*args, **kwargs)

def generate_receipt_number():
    import random
    import string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.drug.name} - {self.quantity} units at {self.unit_price}"