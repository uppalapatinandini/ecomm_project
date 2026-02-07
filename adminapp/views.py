from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from ecommapp.models import VendorProfile
import random

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    vendors = VendorProfile.objects.all()
    return render(request, 'dashboard.html', {
        'vendors': vendors
    })

@user_passes_test(is_admin)
def generate_code(request, vendor_id):
    vendor = VendorProfile.objects.get(id=vendor_id)
    vendor.activation_code = random.randint(100000, 999999)
    vendor.save()
    return redirect('admin_dashboard')  
  