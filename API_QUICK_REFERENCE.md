# API Quick Reference Guide

## Base URL
```
http://localhost:8000/api/
```

## Authentication Header
```
Authorization: Token <your-auth-token>
```

---

## Vendor Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/vendor/register/` | ❌ | Register new vendor |
| POST | `/vendor/login/` | ❌ | Login and get token |
| POST | `/vendor/vendor/details/` | ✅ | Submit shop details |
| GET | `/vendor/vendor/dashboard/` | ✅ | Get dashboard stats |
| GET | `/vendor/vendor/profile/` | ✅ | Get vendor profile |
| GET | `/vendor/vendor/approval-status/` | ✅ | Check approval status |
| GET | `/vendor/user/profile/` | ✅ | Get user info |
| GET | `/vendor/products/` | ✅ | List products |
| POST | `/vendor/products/` | ✅ | Create product |
| GET | `/vendor/products/{id}/` | ✅ | Get product details |
| PUT | `/vendor/products/{id}/` | ✅ | Update product |
| DELETE | `/vendor/products/{id}/` | ✅ | Delete product |
| GET | `/vendor/products/approved/` | ✅ | List approved products |
| GET | `/vendor/products/pending/` | ✅ | List pending products |
| GET | `/vendor/products/blocked/` | ✅ | List blocked products |

---

## Admin Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/admin/dashboard/` | ✅ | Admin dashboard stats |
| GET | `/admin/vendor-requests/` | ✅ | List pending vendors |
| POST | `/admin/vendor-requests/{id}/approve/` | ✅ | Approve vendor |
| POST | `/admin/vendor-requests/{id}/reject/` | ✅ | Reject vendor |
| GET | `/admin/vendors/` | ✅ | List all vendors |
| GET | `/admin/vendors/{id}/detail/` | ✅ | Get vendor details |
| POST | `/admin/vendors/{id}/block/` | ✅ | Block vendor |
| POST | `/admin/vendors/{id}/unblock/` | ✅ | Unblock vendor |
| GET | `/admin/products/` | ✅ | List all products |
| GET | `/admin/products/{id}/detail/` | ✅ | Get product details |
| POST | `/admin/products/{id}/block/` | ✅ | Block product |
| POST | `/admin/products/{id}/unblock/` | ✅ | Unblock product |

---

## Request Examples

### 1. Register Vendor
```bash
POST /api/vendor/register/
Content-Type: application/json

{
  "username": "vendor1",
  "email": "vendor@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

### 2. Login Vendor
```bash
POST /api/vendor/login/
Content-Type: application/json

{
  "username": "vendor1",
  "password": "password123"
}

Response: { "token": "abc123..." }
```

### 3. Submit Vendor Details
```bash
POST /api/vendor/vendor/details/
Content-Type: multipart/form-data
Authorization: Token abc123...

shop_name=My Shop
shop_description=Online store
address=123 Main St
business_type=retail
id_type=gst
id_number=18AABCU9067N1Z5
id_proof_file=<file>
```

### 4. Create Product
```bash
POST /api/vendor/products/
Content-Type: multipart/form-data
Authorization: Token abc123...

name=Product Name
description=Description
price=99.99
quantity=50
status=pending
image=<file>
```

### 5. List Products (with filters)
```bash
GET /api/vendor/products/?status=approved&search=laptop
Authorization: Token abc123...
```

### 6. Get Dashboard
```bash
GET /api/vendor/vendor/dashboard/
Authorization: Token abc123...
```

### 7. Approve Vendor (Admin)
```bash
POST /api/admin/vendor-requests/1/approve/
Content-Type: application/json
Authorization: Token admin_token123...

{
  "reason": "Documents verified"
}
```

### 8. Block Vendor (Admin)
```bash
POST /api/admin/vendors/1/block/
Content-Type: application/json
Authorization: Token admin_token123...

{
  "reason": "Multiple complaints"
}
```

### 9. List Vendors (with filters)
```bash
GET /api/admin/vendors/?status=approved&blocked=false&search=shop
Authorization: Token admin_token123...
```

---

## Query Parameters

### Product List Filters
```
/api/vendor/products/
  ?status=approved       (pending, approved, rejected)
  &search=laptop         (search by name or description)
```

### Admin Vendor Filters
```
/api/admin/vendors/
  ?status=approved       (approved, rejected, pending)
  &blocked=true          (true or false)
  &search=shop_name      (search by name, email, username)
```

### Admin Product Filters
```
/api/admin/products/
  ?status=approved       (pending, approved, rejected)
  &blocked=false         (true or false)
  &search=phone          (search by name or vendor)
  &vendor_id=1           (filter by vendor)
```

---

## Common Response Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not Found (resource doesn't exist) |
| 500 | Server Error |

---

## Error Response Format

```json
{
  "error": "Detailed error message"
}
```

or for field validation errors:

```json
{
  "field_name": [
    "Error message 1",
    "Error message 2"
  ]
}
```

---

## Token Management

### Get Token from Login
```bash
POST /api/vendor/login/
{
  "username": "vendor1",
  "password": "password123"
}

Response: 
{
  "token": "abc123def456..."
}
```

### Alternative Token Endpoint
```bash
POST /api/auth/token-auth/
{
  "username": "admin_user",
  "password": "password123"
}
```

### Using Token in Requests
```bash
curl -H "Authorization: Token abc123def456..." \
     http://localhost:8000/api/vendor/products/
```

---

## Vendor Status Flow

```
User Registered
    ↓
Shop Details Submitted (approval_status = "pending")
    ↓
Admin Reviews Request
    ↓
Approved OR Rejected
    ↓
Vendor Can Manage Products (if approved)
    ↓
Vendor May Be Blocked (if violations occur)
```

---

## Product Status Flow

```
Product Created (status = "pending")
    ↓
Admin Reviews Product (optional)
    ↓
Approved (visible in marketplace)
    ↓
Admin May Block Product (if violations)
```

---

## Response Examples

### Success Response
```json
{
  "message": "Operation successful",
  "vendor": {
    "id": 1,
    "shop_name": "My Shop",
    "approval_status": "approved"
  }
}
```

### Error Response
```json
{
  "error": "Invalid username or password"
}
```

### List Response
```json
[
  {
    "id": 1,
    "name": "Product 1",
    "price": "99.99"
  },
  {
    "id": 2,
    "name": "Product 2",
    "price": "149.99"
  }
]
```

---

## Business Type Choices
- retail
- wholesale
- manufacturer
- service

## ID Type Choices
- gst
- pan

## Status Choices
- pending
- approved
- rejected

---

## Pagination

Default page size: 20 items

```bash
GET /api/vendor/products/?page=1
GET /api/vendor/products/?page=2
```

---

## File Upload Fields

These endpoints accept file uploads (multipart/form-data):
- `POST /api/vendor/vendor/details/` - id_proof_file
- `POST /api/vendor/products/` - image
- `PUT /api/vendor/products/{id}/` - image (optional)

---

## Common Errors

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```
**Solution:** Include `Authorization: Token <token>` header

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```
**Solution:** Use correct user type (admin vs vendor)

### 400 Bad Request
```json
{
  "username": ["A user with that username already exists."]
}
```
**Solution:** Check field values and format

### 404 Not Found
```json
{
  "detail": "Not found."
}
```
**Solution:** Verify resource ID is correct

---

## Testing Quick Commands

### cURL
```bash
# Register
curl -X POST http://localhost:8000/api/vendor/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"v1","email":"v1@test.com","password":"pass123","confirm_password":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/vendor/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"v1","password":"pass123"}'

# Dashboard with token
curl -H "Authorization: Token YOUR_TOKEN" \
  http://localhost:8000/api/vendor/vendor/dashboard/
```

### Python (requests library)
```python
import requests

# Register
requests.post('http://localhost:8000/api/vendor/register/', json={
    'username': 'v1',
    'email': 'v1@test.com',
    'password': 'pass123',
    'confirm_password': 'pass123'
})

# Login
resp = requests.post('http://localhost:8000/api/vendor/login/', json={
    'username': 'v1',
    'password': 'pass123'
})
token = resp.json()['token']

# Dashboard
headers = {'Authorization': f'Token {token}'}
requests.get('http://localhost:8000/api/vendor/vendor/dashboard/', headers=headers)
```

---

## API Documentation Files

1. **API_DOCUMENTATION.md** - Complete endpoint reference with examples
2. **API_SETUP_GUIDE.md** - Detailed setup and integration guide
3. **API_IMPLEMENTATION_SUMMARY.md** - Overview of what's been implemented
4. **Ecommerce_API.postman_collection.json** - Postman collection for testing

---

## Frontend Integration Resources

- All endpoints ready for integration
- CORS configured for localhost:3000 and localhost:8080
- Token-based authentication suitable for SPAs
- No additional setup required on backend

---

## Support

For detailed information, refer to:
- API_DOCUMENTATION.md for endpoint specifications
- API_SETUP_GUIDE.md for integration examples
- Django REST Framework docs: https://www.django-rest-framework.org/
