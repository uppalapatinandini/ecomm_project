# REST API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
All endpoints (except `register` and `login`) require authentication. Use one of the following methods:

### 1. Token Authentication (Recommended)
Include the token in the Authorization header:
```
Authorization: Token <your-auth-token>
```

### 2. Session Authentication
Login first and cookies are automatically included for subsequent requests.

---

## Vendor API Endpoints

### 1. User Registration
**POST** `/api/vendor/register/`

Register a new vendor user account.

**Request:**
```json
{
  "username": "vendor_username",
  "email": "vendor@example.com",
  "password": "securepassword123",
  "confirm_password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user_id": 1,
  "username": "vendor_username",
  "email": "vendor@example.com"
}
```

---

### 2. User Login
**POST** `/api/vendor/login/`

Authenticate vendor and receive authentication token.

**Request:**
```json
{
  "username": "vendor_username",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "abc123def456ghi789",
  "user": {
    "id": 1,
    "username": "vendor_username",
    "email": "vendor@example.com"
  },
  "vendor": {
    "id": 1,
    "status": "pending",
    "is_blocked": false
  }
}
```

---

### 3. Submit Vendor Shop Details
**POST** `/api/vendor/vendor/details/`

Submit shop details for vendor approval.

**Request (multipart/form-data):**
```
shop_name: "My Shop"
shop_description: "Online retail store"
address: "123 Main St, City, State"
business_type: "retail"
id_type: "gst"
id_number: "18AABCU9067N1Z5"
id_proof_file: <file>
```

**Response (201 Created):**
```json
{
  "message": "Vendor profile submitted for approval",
  "vendor": {
    "id": 1,
    "user": {...},
    "shop_name": "My Shop",
    "approval_status": "pending",
    "is_blocked": false,
    ...
  }
}
```

---

### 4. Get Vendor Dashboard
**GET** `/api/vendor/vendor/dashboard/`

Get vendor dashboard with profile and product statistics.

**Response (200 OK):**
```json
{
  "vendor": {
    "id": 1,
    "shop_name": "My Shop",
    "approval_status": "approved",
    "is_blocked": false,
    ...
  },
  "products_count": 10,
  "approved_products": 8,
  "pending_products": 1,
  "blocked_products": 1
}
```

---

### 5. Get Vendor Profile
**GET** `/api/vendor/vendor/profile/`

Get complete vendor profile information.

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "vendor_username",
    "email": "vendor@example.com"
  },
  "shop_name": "My Shop",
  "approval_status": "approved",
  "is_blocked": false,
  "created_at": "2024-01-15T10:30:00Z",
  ...
}
```

---

### 6. Get Approval Status
**GET** `/api/vendor/vendor/approval-status/`

Check vendor approval status.

**Response (200 OK):**
```json
{
  "approval_status": "approved",
  "is_blocked": false,
  "rejection_reason": null,
  "blocked_reason": null
}
```

---

### 7. List Vendor Products
**GET** `/api/vendor/products/`

List all vendor's products.

**Query Parameters:**
- `status`: Filter by status (pending, approved, rejected)
- `search`: Search by product name or description

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "vendor_name": "My Shop",
    "price": "99.99",
    "quantity": 50,
    "status": "approved",
    "is_blocked": false,
    "created_at": "2024-01-15T10:30:00Z"
  },
  ...
]
```

---

### 8. Get Product Details
**GET** `/api/vendor/products/{id}/`

Get detailed information about a specific product.

**Response (200 OK):**
```json
{
  "id": 1,
  "vendor": 1,
  "vendor_name": "My Shop",
  "name": "Product Name",
  "description": "Product description",
  "price": "99.99",
  "quantity": 50,
  "image": "http://example.com/image.jpg",
  "status": "approved",
  "is_blocked": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 9. Create Product
**POST** `/api/vendor/products/`

Add a new product.

**Request (multipart/form-data):**
```
name: "Product Name"
description: "Product description"
price: 99.99
quantity: 50
image: <file>
status: "pending"
```

**Response (201 Created):**
```json
{
  "id": 1,
  "vendor": 1,
  "name": "Product Name",
  "description": "Product description",
  "price": "99.99",
  "quantity": 50,
  "image": "http://example.com/image.jpg",
  "status": "pending",
  "is_blocked": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 10. Update Product
**PUT/PATCH** `/api/vendor/products/{id}/`

Update product details.

**Request:**
```json
{
  "name": "Updated Product Name",
  "price": "109.99",
  "quantity": 45
}
```

**Response (200 OK):** Updated product object

---

### 11. Delete Product
**DELETE** `/api/vendor/products/{id}/`

Delete a product.

**Response (204 No Content):**
```json
{
  "message": "Product deleted successfully"
}
```

---

### 12. Get Approved Products
**GET** `/api/vendor/products/approved/`

List only approved products.

**Response (200 OK):** Array of approved products

---

### 13. Get Pending Products
**GET** `/api/vendor/products/pending/`

List only pending approval products.

**Response (200 OK):** Array of pending products

---

### 14. Get Blocked Products
**GET** `/api/vendor/products/blocked/`

List only blocked products.

**Response (200 OK):** Array of blocked products

---

### 15. Get User Profile
**GET** `/api/vendor/user/profile/`

Get current user profile information.

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "vendor_username",
  "email": "vendor@example.com",
  "first_name": "",
  "last_name": ""
}
```

---

## Admin API Endpoints

### 1. Admin Dashboard
**GET** `/api/admin/dashboard/`

Get admin dashboard statistics.

**Response (200 OK):**
```json
{
  "vendors": {
    "total": 50,
    "pending": 5,
    "approved": 40,
    "blocked": 5
  },
  "products": {
    "total": 200,
    "pending": 20,
    "approved": 170,
    "blocked": 10
  }
}
```

---

### 2. List Vendor Requests (Pending)
**GET** `/api/admin/vendor-requests/`

List all pending vendor approval requests.

**Query Parameters:**
- `search`: Search by shop name or owner email

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user_username": "vendor_username",
    "user_email": "vendor@example.com",
    "shop_name": "My Shop",
    "shop_description": "Online retail store",
    "address": "123 Main St, City, State",
    "business_type": "retail",
    "approval_status": "pending",
    "created_at": "2024-01-15T10:30:00Z",
    "approval_logs": [...]
  },
  ...
]
```

---

### 3. Approve Vendor
**POST** `/api/admin/vendor-requests/{id}/approve/`

Approve a pending vendor.

**Request:**
```json
{
  "reason": "All documents verified successfully"
}
```

**Response (200 OK):**
```json
{
  "message": "Vendor approved successfully",
  "vendor": {...}
}
```

---

### 4. Reject Vendor
**POST** `/api/admin/vendor-requests/{id}/reject/`

Reject a pending vendor.

**Request:**
```json
{
  "reason": "Invalid business documents provided"
}
```

**Response (200 OK):**
```json
{
  "message": "Vendor rejected successfully",
  "vendor": {...}
}
```

---

### 5. List All Vendors
**GET** `/api/admin/vendors/`

List all vendors with filtering options.

**Query Parameters:**
- `status`: Filter by approval status (approved, rejected, pending)
- `blocked`: Filter by blocked status (true/false)
- `search`: Search by shop name, owner email, or username

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "shop_name": "My Shop",
    "user_email": "vendor@example.com",
    "approval_status": "approved",
    "is_blocked": false,
    "created_at": "2024-01-15T10:30:00Z"
  },
  ...
]
```

---

### 6. Get Vendor Details
**GET** `/api/admin/vendors/{id}/detail/`

Get detailed information about a specific vendor.

**Response (200 OK):**
```json
{
  "id": 1,
  "user_username": "vendor_username",
  "user_email": "vendor@example.com",
  "shop_name": "My Shop",
  "shop_description": "Online retail store",
  "address": "123 Main St, City, State",
  "business_type": "retail",
  "approval_status": "approved",
  "is_blocked": false,
  "blocked_reason": null,
  "approval_logs": [...]
}
```

---

### 7. Block Vendor
**POST** `/api/admin/vendors/{id}/block/`

Block a vendor account.

**Request:**
```json
{
  "reason": "Multiple complaints from customers"
}
```

**Response (200 OK):**
```json
{
  "message": "Vendor blocked successfully",
  "vendor": {...}
}
```

---

### 8. Unblock Vendor
**POST** `/api/admin/vendors/{id}/unblock/`

Unblock a previously blocked vendor.

**Request:**
```json
{
  "reason": "Issue resolved after investigation"
}
```

**Response (200 OK):**
```json
{
  "message": "Vendor unblocked successfully",
  "vendor": {...}
}
```

---

### 9. List All Products
**GET** `/api/admin/products/`

List all products with filtering options.

**Query Parameters:**
- `status`: Filter by status (pending, approved, rejected)
- `blocked`: Filter by blocked status (true/false)
- `search`: Search by product name or vendor name
- `vendor_id`: Filter by vendor ID

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Product Name",
    "vendor": 1,
    "vendor_name": "My Shop",
    "price": "99.99",
    "quantity": 50,
    "is_blocked": false,
    "created_at": "2024-01-15T10:30:00Z"
  },
  ...
]
```

---

### 10. Get Product Details
**GET** `/api/admin/products/{id}/detail/`

Get detailed information about a specific product.

**Response (200 OK):**
```json
{
  "id": 1,
  "vendor": 1,
  "vendor_shop_name": "My Shop",
  "vendor_owner": "vendor_username",
  "name": "Product Name",
  "description": "Product description",
  "price": "99.99",
  "quantity": 50,
  "image": "http://example.com/image.jpg",
  "status": "approved",
  "is_blocked": false,
  "blocked_reason": null,
  "approval_logs": [...]
}
```

---

### 11. Block Product
**POST** `/api/admin/products/{id}/block/`

Block a product from marketplace.

**Request:**
```json
{
  "reason": "Product violates marketplace policies"
}
```

**Response (200 OK):**
```json
{
  "message": "Product blocked successfully",
  "product": {...}
}
```

---

### 12. Unblock Product
**POST** `/api/admin/products/{id}/unblock/`

Unblock a previously blocked product.

**Request:**
```json
{
  "reason": "Issue has been resolved"
}
```

**Response (200 OK):**
```json
{
  "message": "Product unblocked successfully",
  "product": {...}
}
```

---

## Error Responses

All endpoints return error responses with appropriate HTTP status codes:

**400 Bad Request:**
```json
{
  "error": "Description of the error"
}
```

**401 Unauthorized:**
```json
{
  "error": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "error": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "error": "Not found."
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error"
}
```

---

## Testing the API

### Using cURL

```bash
# Register vendor
curl -X POST http://localhost:8000/api/vendor/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "vendor_username",
    "email": "vendor@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
  }'

# Login
curl -X POST http://localhost:8000/api/vendor/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "vendor_username",
    "password": "securepassword123"
  }'

# Get dashboard (with token)
curl -X GET http://localhost:8000/api/vendor/vendor/dashboard/ \
  -H "Authorization: Token abc123def456ghi789"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/vendor/register/", json={
    "username": "vendor_username",
    "email": "vendor@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
})

# Login
response = requests.post(f"{BASE_URL}/vendor/login/", json={
    "username": "vendor_username",
    "password": "securepassword123"
})
token = response.json()["token"]

# Get dashboard
headers = {"Authorization": f"Token {token}"}
response = requests.get(f"{BASE_URL}/vendor/vendor/dashboard/", headers=headers)
```

### Using Postman

1. Import the API collection from the included Postman export
2. Set `{{base_url}}` variable to `http://localhost:8000/api`
3. Set `{{token}}` variable after logging in
4. Use the pre-configured requests

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000`
- `http://localhost:8080`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:8080`

To add more origins, update the `CORS_ALLOWED_ORIGINS` in `settings.py`.
