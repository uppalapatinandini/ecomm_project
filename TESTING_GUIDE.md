# Testing Guide - E-Commerce Platform

## Quick Start

### 1. Start the Development Server
```bash
python manage.py runserver
```

The server will be available at: `http://127.0.0.1:8000/`

### 2. Create Admin User (Superuser)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

---

## Testing Vendor Workflow

### Step 1: Vendor Registration

**URL:** `http://127.0.0.1:8000/register/`

**What to do:**
1. Click "New vendor? Register"
2. Fill in credentials:
   - Username: `vendor1`
   - Email: `vendor1@example.com` (any email)
   - Password: `TestPass123!`
   - Confirm Password: `TestPass123!`
3. Click "Send OTP"

**Expected Result:**
- Form validates inputs
- In development, check console or email backend for OTP
- If using EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend', OTP appears in console

### Step 2: Verify OTP

**URL:** `http://127.0.0.1:8000/verify-otp/`

**What to do:**
1. From the OTP email/console, copy the 6-digit OTP
2. Enter in the OTP field
3. Click "Verify OTP"

**Expected Result:**
- Redirected to `/vendor-details/`
- Session created with vendor_user_id

### Step 3: Complete Shop Details

**URL:** `http://127.0.0.1:8000/vendor-details/`

**What to do:**
1. Fill in shop details:
   - Shop Name: `Tech Gadgets Store`
   - Shop Description: `We sell latest tech gadgets`
   - Address: `123 Main Street, City`
   - Business Type: `Retail`
   - ID Type: `GST`
   - GST/PAN Number: `29AABGN6234G1Z0`
   - Upload a file as ID Proof
2. Click "Complete Registration"

**Expected Result:**
- VendorProfile created with approval_status = 'pending'
- Redirected to login page
- User can log in now

### Step 4: Check Approval Status

**URL:** `http://127.0.0.1:8000/` (Vendor Login)

**What to do:**
1. Log in with vendor credentials:
   - Username: `vendor1`
   - Password: `TestPass123!`
2. Click Login

**Expected Result:**
- System checks approval status
- Shows "Approval Pending" page
- Displays shop details and approval status
- Cannot access dashboard yet

---

## Testing Admin Approval Workflow

### Step 1: Admin Login

**URL:** `http://127.0.0.1:8000/main/login/`

**What to do:**
1. Log in with superuser credentials:
   - Username: (your superuser username)
   - Password: (your superuser password)
2. Click Login

**Expected Result:**
- Redirected to `/main/` (admin dashboard)
- Shows statistics:
  - Total vendors: 1
  - Pending vendors: 1
  - Approved vendors: 0
  - Products count: 0

### Step 2: Create another vendor or use existing

If you followed Step 1-3 above, you have 1 vendor with status "pending"

### Step 3: Review Vendor Request

**URL:** `http://127.0.0.1:8000/main/vendor-requests/`

**What to do:**
1. See list of vendor requests
2. Click on vendor with "Pending" status
3. View `/main/vendor-requests/<vendor_id>/`

**Expected Result:**
- Shows vendor information
- Business details form
- Two action buttons: "Approve" and "Reject"

### Step 4: Approve Vendor

**URL:** `http://127.0.0.1:8000/main/vendor-requests/<vendor_id>/approve/`

**What to do:**
1. (Optional) Add approval notes
2. Click "Approve Vendor"

**Expected Result:**
- Vendor approval_status changes to "approved"
- Approval log created
- Vendor can now access dashboard

### Step 5: Vendor Can Now Access Dashboard

**Back as Vendor:**
1. Log in again with vendor credentials
2. Visit `http://127.0.0.1:8000/vendor/`

**Expected Result:**
- Vendor Dashboard loads
- "No products yet" message
- Button to "Add Your First Product"
- Can now add, edit, delete products

---

## Testing Vendor Management

### Step 1: View All Vendors

**URL:** `http://127.0.0.1:8000/main/vendors/`

**What to do:**
1. See list of all vendors with:
   - Shop name
   - Owner name
   - Approval status
   - Block status

**Expected Result:**
- Table shows vendor1
- Status: Approved
- Block Status: Active
- Action buttons: View, Block

### Step 2: Block a Vendor

**URL:** `http://127.0.0.1:8000/main/vendors/<vendor_id>/block/`

**What to do:**
1. Click "Block" button next to vendor
2. Enter blocking reason: `Violated terms of service`
3. Click "Block Vendor"

**Expected Result:**
- Vendor is_blocked = True
- blocked_reason saved
- All vendor's products also blocked
- Vendor sees "Account Blocked" message

### Step 3: Unblock a Vendor

**URL:** `http://127.0.0.1:8000/main/vendors/<vendor_id>/unblock/`

**What to do:**
1. Click "Unblock" button next to blocked vendor
2. (Optional) Add unblocking notes
3. Click "Unblock Vendor"

**Expected Result:**
- Vendor is_blocked = False
- Vendor can access dashboard again

---

## Testing Product Management

### Step 1: Add Products (as Vendor)

**URL:** `http://127.0.0.1:8000/products/add/`

**What to do:**
1. Log in as vendor (approved)
2. Click "Add Your First Product"
3. Fill in:
   - Product Name: `iPhone 15 Pro`
   - Description: `Latest iPhone with advanced features`
   - Price: `79999`
   - Quantity: `10`
   - Image: (optional)
4. Click "Add Product"

**Expected Result:**
- Product created
- Redirected to vendor dashboard
- Product appears in list

### Step 2: Edit Product

**As Vendor:**
1. Click "Edit" button on product
2. Change price or quantity
3. Click "Update Product"

**Expected Result:**
- Product updated
- Redirected to dashboard

### Step 3: Admin View All Products

**As Admin:**
**URL:** `http://127.0.0.1:8000/main/products/`

**What to do:**
1. See list of all products from all vendors
2. Filter by vendor, product name
3. Search for products

**Expected Result:**
- Table shows products with:
  - Product name
  - Vendor name
  - Price
  - Stock quantity
  - Status (Active/Blocked)
  - Actions (View, Block/Unblock buttons)

### Step 4: Block a Product

**As Admin:**
**URL:** `http://127.0.0.1:8000/main/products/<product_id>/block/`

**What to do:**
1. Click "Block" button
2. Enter reason: `Violates trademark`
3. Click "Block Product"

**Expected Result:**
- Product is_blocked = True
- Product no longer visible to customers
- Vendor sees "Blocked" badge in dashboard

### Step 5: Unblock Product

Similar to unblock vendor - product becomes available again.

---

## Testing Rejections

### Admin Reject Vendor

**URL:** `http://127.0.0.1:8000/main/vendor-requests/<vendor_id>/reject/`

**What to do:**
1. From vendor requests list
2. Click "Reject" button
3. Enter reason: `Documents not verified properly`
4. Click "Reject Vendor"

**Expected Result:**
- approval_status = "rejected"
- rejection_reason saved
- When vendor logs in, sees rejection message with reason
- Cannot access dashboard

---

## Database Verification

### Check Vendor Data
```bash
python manage.py shell
```

```python
from ecommapp.models import VendorProfile, Product

# View all vendors
vendors = VendorProfile.objects.all()
for v in vendors:
    print(f"{v.shop_name} - {v.approval_status} - Blocked: {v.is_blocked}")

# View all products
products = Product.objects.all()
for p in products:
    print(f"{p.name} - ₹{p.price} - {p.vendor.shop_name}")

# View approval logs
from mainApp.models import VendorApprovalLog
logs = VendorApprovalLog.objects.all()
for log in logs:
    print(f"{log.vendor.shop_name} - {log.action} by {log.admin_user.username}")
```

Exit shell: `exit()`

---

## Troubleshooting

### Issue: OTP not received
- **Solution:** Check DJANGO_CORE_MAIL backend in settings.py
- For development, use: `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
- OTP will appear in console output

### Issue: "Template not found" error
- **Solution:** Ensure templates are in correct subdirectories
- Vendor templates: `ecommapp/templates/ecommapp/`
- Admin templates: `mainApp/templates/mainApp/`

### Issue: Login redirecting to wrong place
- **Solution:** Check URL configuration
- Vendor login (login view): `/` 
- Admin login: `/main/login/`
- Both are separate

### Issue: Cannot upload files
- **Solution:** Ensure MEDIA_ROOT and MEDIA_URL are configured
- Create `media/vendor_docs/` directory
- Check file upload permissions

### Issue: Approval status not changing
- **Solution:** Ensure VendorProfile model has approval_status field
- Check database has correct schema (run migrations if needed)

---

## Quick Test Summary

✓ Register vendor  
✓ Verify OTP  
✓ Submit shop details  
✓ Admin approves vendor  
✓ Vendor accesses dashboard  
✓ Vendor adds products  
✓ Admin blocks/unblocks vendor  
✓ Admin blocks/unblocks products  
✓ Check approval logs  

If all steps pass, your application is working correctly!

---

## Performance Tips

- Use browser Developer Tools (F12) to check:
  - Console for JavaScript errors
  - Network tab to see API calls
  - Storage to check sessions

- Check server console for Django errors (if running in foreground)

- Use Django Debug Toolbar (if installed) to debug queries

---

## Support

For issues or questions:
1. Check console output for error messages
2. Review FIX_SUMMARY.md for architecture overview
3. Verify database has been migrated: `python manage.py migrate`
4. Check INSTALLED_APPS includes all required apps
