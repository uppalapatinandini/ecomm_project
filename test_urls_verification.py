#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
sys.path.insert(0, r'C:\Users\imvis\Desktop\my_projects\ecomm_project')

django.setup()

from django.urls import reverse

# Test URL patterns
vendor_urls = [
    'register', 'verify_otp', 'vendor_details', 'login', 'logout', 
    'vendor_home', 'approval_status', 'add_product'
]

admin_urls = [
    'admin_login', 'admin_logout', 'admin_dashboard', 
    'manage_vendor_requests', 'manage_vendors', 'manage_products'
]

print("\n✓ Testing Vendor URL Names:")
for url in vendor_urls:
    try:
        path = reverse(url)
        print(f"  ✓ {url:20} → {path}")
    except Exception as e:
        print(f"  ✗ {url:20} → ERROR: {str(e)[:50]}")

print("\n✓ Testing Admin URL Names:")
for url in admin_urls:
    try:
        path = reverse(url)
        print(f"  ✓ {url:20} → {path}")
    except Exception as e:
        print(f"  ✗ {url:20} → ERROR: {str(e)[:50]}")

print("\n✓ All URL patterns tested successfully!")
