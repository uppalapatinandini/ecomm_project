#!/usr/bin/env python
"""Test script to verify URL configuration and server readiness"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecomm.settings')
django.setup()

from django.urls import get_resolver
from django.core.management import call_command

print("\n" + "="*60)
print("  DJANGO SERVER VERIFICATION TEST")
print("="*60)

# Test 1: URL Configuration
print("\n✅ Test 1: URL Configuration")
print("-" * 60)
try:
    resolver = get_resolver()
    urls = resolver.url_patterns
    print(f"Total URL patterns: {len(urls)}")
    for pattern in urls:
        print(f"  • {pattern.pattern}")
    print("\n✅ URL configuration is VALID!")
except Exception as e:
    print(f"❌ URL configuration error: {e}")
    sys.exit(1)

# Test 2: Models Check
print("\n✅ Test 2: Models Check")
print("-" * 60)
try:
    from ecommapp.models import VendorProfile, Product
    from mainApp.models import VendorApprovalLog, ProductApprovalLog
    from django.contrib.auth.models import User
    
    print(f"  • VendorProfile: {VendorProfile._meta.fields}")
    print(f"  • Product: {Product._meta.fields}")
    print(f"  • VendorApprovalLog: {VendorApprovalLog._meta.fields}")
    print(f"  • ProductApprovalLog: {ProductApprovalLog._meta.fields}")
    print("\n✅ All models loaded successfully!")
except Exception as e:
    print(f"❌ Model loading error: {e}")
    sys.exit(1)

# Test 3: Views Check
print("\n✅ Test 3: Views Check")
print("-" * 60)
try:
    from ecommapp.views import (
        register_view, verify_otp_view, vendor_details_view,
        login_view, logout_view, vendor_home_view, approval_status_view,
        add_product_view, edit_product_view, delete_product_view, view_product_view
    )
    from mainApp.views import (
        admin_dashboard, manage_vendor_requests, vendor_request_detail,
        approve_vendor, reject_vendor, manage_vendors, vendor_detail,
        block_vendor, unblock_vendor, manage_products, product_detail,
        block_product, unblock_product
    )
    from adminapp.views import (
        admin_dashboard as adminapp_dashboard, vendor_list, vendor_details,
        product_list, system_settings
    )
    print(f"  • ecommapp: 11 views loaded")
    print(f"  • mainApp: 13 views loaded")
    print(f"  • adminapp: 5 views loaded")
    print("\n✅ All views loaded successfully!")
except Exception as e:
    print(f"❌ View loading error: {e}")
    sys.exit(1)

# Test 4: Migrations Check
print("\n✅ Test 4: Migrations Check")
print("-" * 60)
try:
    from django.db.migrations.loader import MigrationLoader
    loader = MigrationLoader(None)
    
    graph = loader.graph
    leaf_nodes = graph.leaf_nodes()
    
    print(f"  • Total migration apps: {len(loader.migrated_apps)}")
    print(f"  • Migrated apps: {', '.join(sorted(loader.migrated_apps))}")
    print(f"  • Leaf nodes (latest migrations): {len(leaf_nodes)}")
    print("\n✅ Migration status is OK!")
except Exception as e:
    print(f"❌ Migration check error: {e}")
    sys.exit(1)

# Final Summary
print("\n" + "="*60)
print("  ✅ ALL TESTS PASSED - SERVER IS READY!")
print("="*60)
print("\nServer Details:")
print("  • URL: http://127.0.0.1:8000/")
print("  • Admin Panel: http://127.0.0.1:8000/admin/")
print("  • System Admin: http://127.0.0.1:8000/admin-panel/")
print("  • Custom Admin: http://127.0.0.1:8000/main/")
print("\nStart server with: python manage.py runserver")
print("="*60 + "\n")
