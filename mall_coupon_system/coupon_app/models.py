from django.db import models
from django.contrib.auth.models import User

class Store(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    store_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('store_manager', 'Store Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username}) - {self.user_type}"

class Purchase(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    amount_spent = models.FloatField()
    visit_count = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} at {self.store.name}"

class Coupon(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    code = models.CharField(max_length=20)  # <-- this line is critical
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    issued_at = models.DateTimeField(auto_now_add=True)
    validity_date = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"{self.code} for {self.user.user.username}"

class UploadedDataset(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dataset for {self.store.name}"
