from django.db import models
from django.contrib.auth.models import User

class VendorProfile(models.Model):
    BUSINESS_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('manufacturer', 'Manufacturer'),
        ('service', 'Service'),
    ]

    ID_PROOF_CHOICES = [
        ('gst', 'GST'),
        ('pan', 'PAN'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField()
    address = models.TextField()
    business_type = models.CharField(max_length=20, choices=BUSINESS_CHOICES)
    id_type = models.CharField(max_length=10, choices=ID_PROOF_CHOICES)
    id_number = models.CharField(max_length=50)
    id_proof_file = models.FileField(upload_to='vendor_docs/')
    is_approved = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.shop_name
    


class VendorProfile(models.Model):
    BUSINESS_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('manufacturer', 'Manufacturer'),
        ('service', 'Service'),
    ]

    ID_PROOF_CHOICES = [
        ('gst', 'GST'),
        ('pan', 'PAN'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    shop_description = models.TextField()
    address = models.TextField()
    business_type = models.CharField(max_length=20, choices=BUSINESS_CHOICES)
    id_type = models.CharField(max_length=10, choices=ID_PROOF_CHOICES)
    id_number = models.CharField(max_length=50)
    id_proof_file = models.FileField(upload_to='vendor_docs/')
    is_approved = models.BooleanField(default=False)  # <-- THIS LINE

    def __str__(self):
        return self.shop_name


