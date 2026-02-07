# E-Commerce Platform - Project Structure & Architecture

## Overview

This Django-based e-commerce platform has been restructured into three distinct applications with clear responsibilities:

1. **ecommapp** - Vendor application (vendor registration, products, approval status)
2. **mainApp** - Custom admin app (vendor request management, approvals, blocking/unblocking)
3. **adminapp** - Default admin app (system-wide overview and management)

---

## Application Structure

### 1. ECOMMAPP (Vendor Application)

**Purpose:** Vendor registration, vendor dashboard, and product management

#### Models

##### VendorProfile
- **Fields:**
  - `user` (OneToOneField) - Link to Django User
  - `shop_name`, `shop_description`, `address`
  - `business_type` - Choices: retail, wholesale, manufacturer, service
  - `id_type`, `id_number`, `id_proof_file` - ID verification
  - `approval_status` - Choices: pending, approved, rejected
  - `rejection_reason` - Text explaining rejection
  - `is_blocked` - Boolean flag for vendor blocking
  - `blocked_reason` - Text explaining block
  - `created_at`, `updated_at` - Timestamps

- **Features:**
  - Default approval_status is 'pending'
  - Has backward compatibility property `is_approved`
  - Related to: Product (through `products` relation), VendorApprovalLog (through `approval_logs`)

##### Product
- **Fields:**
  - `vendor` (ForeignKey) - Link to VendorProfile
  - `name`, `description`, `price`, `quantity`, `image`
  - `status` - Choices: active, inactive
  - `is_blocked` - Boolean flag for product blocking
  - `blocked_reason` - Text explaining block
  - `created_at`, `updated_at` - Timestamps

- **Features:**
  - Each product belongs to a vendor
  - Can be blocked/unblocked by admins
  - Related to: ProductApprovalLog (through `approval_logs`)

#### Views

| View | URL | Access | Purpose |
|------|-----|--------|---------|
| `register_view` | `/register/` | Public | Vendor registration with OTP verification |
| `verify_otp_view` | `/verify-otp/` | Public | OTP verification during registration |
| `vendor_details_view` | `/vendor-details/` | Public (Session) | Submit shop details |
| `login_view` | `/` | Public | Vendor login |
| `logout_view` | `/logout/` | Authenticated | Vendor logout |
| `vendor_home_view` | `/vendor/` | Authenticated | Main vendor dashboard, shows approval status or products |
| `approval_status_view` | `/approval-status/` | Authenticated | View approval status (pending/rejected) |
| `add_product_view` | `/products/add/` | Authenticated, Approved | Add new product |
| `edit_product_view` | `/products/<id>/edit/` | Authenticated, Approved | Edit product details |
| `delete_product_view` | `/products/<id>/delete/` | Authenticated, Approved | Delete product |
| `view_product_view` | `/products/<id>/` | Authenticated, Approved | View product details |

#### Workflow

1. **Registration Flow:**
   - Vendor fills registration form
   - OTP sent to email
   - OTP verified, user account created
   - Vendor enters shop details
   - VendorProfile created with `approval_status='pending'`

2. **Approval Status Flow:**
   - If `approval_status == 'pending'` → Show approval status page
   - If `approval_status == 'rejected'` → Show rejection reason
   - If `approval_status == 'approved'` → Show vendor dashboard with products
   - If `is_blocked == True` → Show vendor blocked page

3. **Product Management:**
   - Only approved vendors can add/edit/delete products
   - Admins can block/unblock products
   - Vendors can view blocked products and reasons

---

### 2. MAINAPP (Custom Admin Application)

**Purpose:** Vendor request approval, vendor management, and product oversight

#### Models

##### VendorApprovalLog
- **Fields:**
  - `vendor` (ForeignKey) - VendorProfile
  - `admin_user` (ForeignKey) - Django User (admin)
  - `action` - Choices: approved, rejected, blocked, unblocked, reviewed
  - `reason` - Text field for action reason
  - `timestamp` - Auto timestamp

- **Purpose:** Audit trail for all vendor-related admin actions

##### ProductApprovalLog
- **Fields:**
  - `product` (ForeignKey) - Product
  - `admin_user` (ForeignKey) - Django User (admin)
  - `action` - Choices: blocked, unblocked
  - `reason` - Text field for action reason
  - `timestamp` - Auto timestamp

- **Purpose:** Audit trail for all product-related admin actions

#### Views

| View | URL | Access | Purpose |
|------|-----|--------|---------|
| `admin_dashboard` | `/main/` | Admin | Main dashboard with statistics |
| `manage_vendor_requests` | `/main/vendor-requests/` | Admin | View pending/all vendor requests |
| `vendor_request_detail` | `/main/vendor-requests/<id>/` | Admin | Detailed vendor request info |
| `approve_vendor` | `/main/vendor-requests/<id>/approve/` | Admin | Approve vendor registration |
| `reject_vendor` | `/main/vendor-requests/<id>/reject/` | Admin | Reject vendor registration |
| `manage_vendors` | `/main/vendors/` | Admin | Search and manage all vendors |
| `vendor_detail` | `/main/vendors/<id>/` | Admin | Vendor details and actions |
| `block_vendor` | `/main/vendors/<id>/block/` | Admin | Block a vendor (and products) |
| `unblock_vendor` | `/main/vendors/<id>/unblock/` | Admin | Unblock a vendor |
| `manage_products` | `/main/products/` | Admin | Search and manage all products |
| `product_detail` | `/main/products/<id>/` | Admin | Product details |
| `block_product` | `/main/products/<id>/block/` | Admin | Block a product |
| `unblock_product` | `/main/products/<id>/unblock/` | Admin | Unblock a product |

#### Features

1. **Vendor Request Management:**
   - View pending vendor registrations
   - Filter by approval status (pending, approved, rejected)
   - Approve or reject with reason
   - View approval history

2. **Vendor Management:**
   - Search vendors by name, username, or email
   - Filter by approval status
   - Filter by blocked status
   - View vendor details and products
   - Block/unblock vendors with reasons
   - Blocking a vendor blocks all their products

3. **Product Management:**
   - View all products from all vendors
   - Search by product name or description
   - Filter by vendor and blocked status
   - Block/unblock products with reasons
   - View blocking history

---

### 3. ADMINAPP (Default Admin Application)

**Purpose:** System-wide overview and general administration

#### Views

| View | URL | Access | Purpose |
|------|-----|--------|---------|
| `admin_dashboard` | `/admin-panel/` | Admin | High-level platform statistics |
| `vendor_list` | `/admin-panel/vendors/` | Admin | List all vendors with filters |
| `vendor_details` | `/admin-panel/vendors/<id>/` | Admin | Vendor details and stats |
| `product_list` | `/admin-panel/products/` | Admin | List all products |
| `system_settings` | `/admin-panel/settings/` | Admin | System settings (future expansion) |

#### Features

- Platform overview with statistics
- Recent vendor and product lists
- Vendor management interface
- Product overview
- Links to detailed management in mainApp

---

## User Roles & Access Control

### 1. Vendor (ecommapp users)
- **After login:**
  - If `approval_status != 'approved'` → Approve status page
  - Can see rejection reason if rejected
  - Can check approval status
- **After approval:**
  - Access vendor dashboard
  - Add/edit/delete products
  - View product blocking status
- **If blocked:**
  - Cannot access dashboard
  - See blocking reason

### 2. Admin (mainApp users)
- **Must be:** `is_superuser` or `is_staff`
- **Can do:**
  - Approve/reject vendor registrations
  - Block/unblock vendors
  - Block/unblock products
  - View all vendor and product data
  - Access approval history

### 3. Django Superuser (adminapp)
- **Has full access to Django admin panel**
- **Can also use:** default admin dashboard

---

## Approval Workflow

### Vendor Approval Workflow

1. **Registration Phase**
   ```
   Vendor → Register → OTP Verify → Submit Shop Details → Created (pending)
   ```

2. **Admin Review Phase**
   ```
   Admin reviews request → Approves → vendor.approval_status = 'approved'
                       → Rejects → vendor.approval_status = 'rejected' + reason
   ```

3. **Vendor Access Phase**
   ```
   If approved → Access dashboard & manage products
   If rejected → See rejection reason, can register again (new account)
   If blocked → Cannot access anything, see block reason
   ```

### Vendor & Product Blocking Workflow

1. **Vendor Blocking**
   ```
   Admin blocks vendor → vendor.is_blocked = True + reason
                      → All vendor products also blocked
   Admin unblocks → vendor.is_blocked = False
   ```

2. **Product Blocking**
   ```
   Admin blocks product → product.is_blocked = True + reason
   Admin unblocks → product.is_blocked = False
   ```

---

## Database Models Summary

```
User (Django)
├── VendorProfile (1:1)
│   ├── approval_status: pending/approved/rejected
│   ├── is_blocked: True/False
│   └── products (1:N) → Product
│       └── is_blocked: True/False
└── (Admin-related logs reference User)

VendorApprovalLog (tracks vendor approvals/rejections/blocks)
ProductApprovalLog (tracks product blocks/unblocks)
```

---

## URL Structure

### Vendor URLs (ecommapp)
```
/                                    - Login
/register/                           - Register
/verify-otp/                         - Verify OTP
/vendor-details/                     - Submit shop details
/logout/                             - Logout
/vendor/                             - Vendor home/dashboard
/approval-status/                    - Check approval status
/products/add/                       - Add product
/products/<id>/                      - View product
/products/<id>/edit/                 - Edit product
/products/<id>/delete/               - Delete product
```

### Admin URLs (mainApp)
```
/main/                               - Dashboard
/main/vendor-requests/               - Manage vendor requests
/main/vendor-requests/<id>/          - View request details
/main/vendor-requests/<id>/approve/  - Approve
/main/vendor-requests/<id>/reject/   - Reject
/main/vendors/                       - Manage vendors
/main/vendors/<id>/                  - Vendor details
/main/vendors/<id>/block/            - Block vendor
/main/vendors/<id>/unblock/          - Unblock vendor
/main/products/                      - Manage products
/main/products/<id>/                 - Product details
/main/products/<id>/block/           - Block product
/main/products/<id>/unblock/         - Unblock product
```

### System Admin URLs (adminapp)
```
/admin-panel/                        - Dashboard
/admin-panel/vendors/                - Vendor list
/admin-panel/vendors/<id>/           - Vendor details
/admin-panel/products/               - Product list
/admin-panel/settings/               - System settings
```

### Django Admin
```
/admin/                              - Django admin panel
```

---

## Templates Required

### Vendor Templates (ecommapp/templates/ecommapp/)
- `login.html` - Login form
- `register.html` - Registration form
- `verify_otp.html` - OTP verification
- `vendor_details.html` - Shop details form
- `vendor_dashboard.html` - Main vendor dashboard (products list)
- `approval_status.html` - Shows pending/rejected status
- `vendor_blocked.html` - Shows vendor blocked message
- `add_product.html` - Add product form
- `edit_product.html` - Edit product form
- `product_detail.html` - View product details

### Admin Templates (mainApp/templates/mainApp/)
- `admin_dashboard.html` - Statistics dashboard
- `manage_vendor_requests.html` - List vendor requests
- `vendor_request_detail.html` - Detailed request view
- `approve_vendor.html` - Approval confirmation
- `reject_vendor.html` - Rejection form
- `manage_vendors.html` - List all vendors
- `vendor_detail.html` - Vendor detailed view
- `block_vendor.html` - Block confirmation
- `unblock_vendor.html` - Unblock confirmation
- `manage_products.html` - List all products
- `product_detail.html` - Product detailed view
- `block_product.html` - Block product confirmation
- `unblock_product.html` - Unblock product confirmation

### System Admin Templates (adminapp/templates/adminapp/)
- `dashboard.html` - Overview dashboard
- `vendor_list.html` - Vendor list
- `vendor_details.html` - Vendor details
- `product_list.html` - Product list
- `system_settings.html` - Settings page

---

## Key Features Implemented

✅ **Vendor Registration**
- OTP-based registration
- Shop details submission
- ID verification document upload

✅ **Approval Status Tracking**
- Pending/Approved/Rejected states
- Rejection reasons visible to vendors
- Vendor blocked state with blocking reasons

✅ **Product Management**
- Vendors can add/edit/delete products (only if approved)
- Admins can block/unblock products
- Product blocking reasons tracked

✅ **Admin Controls**
- Approve/reject vendor registrations
- Block/unblock vendors
- Block/unblock products
- Audit logs for all actions

✅ **Search & Filter**
- Search vendors by name/email/username
- Search products by name/description
- Filter by approval status
- Filter by blocked status

---

## Migration Notes

After pulling these changes:

1. **Create and apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Expected migrations:**
   - ecommapp: Updated VendorProfile with new fields, new Product model
   - mainApp: Replace VendorRequest with VendorApprovalLog and ProductApprovalLog

3. **Admin setup:**
   - Create superuser if not exists: `python manage.py createsuperuser`
   - Access Django admin at `/admin/`
   - Access mainApp admin at `/main/`
   - Access adminapp at `/admin-panel/`

---

## Testing Checklist

- [ ] Vendor registration with OTP
- [ ] Pending approval status page
- [ ] Admin approval of vendor
- [ ] Vendor dashboard after approval
- [ ] Product add/edit/delete (approved vendors only)
- [ ] Vendor blocking (and product blocking cascade)
- [ ] Product blocking individually
- [ ] Rejection workflow with reasons
- [ ] Search and filter functionality
- [ ] Approval history/audit logs
