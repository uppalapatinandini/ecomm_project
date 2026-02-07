# API Setup and Running Guide

## Quick Start

### 1. Start the Development Server
```bash
cd c:\Users\imvis\Desktop\my_projects\ecomm_project
python manage.py runserver
```

The server will start at `http://localhost:8000`

### 2. API Base URL
```
http://localhost:8000/api/
```

---

## Features Overview

### Vendor Features
- ✅ User registration and login
- ✅ Submit vendor shop details for approval
- ✅ View approval status
- ✅ Complete product management (CRUD)
- ✅ Product filtering by status
- ✅ Dashboard with product statistics
- ✅ User profile management

### Admin Features
- ✅ Vendor approval request management
- ✅ Approve/reject vendor registrations
- ✅ All vendor management (view, block, unblock)
- ✅ Product management (view, block, unblock)
- ✅ Admin dashboard with statistics
- ✅ Activity logging for all actions
- ✅ Advanced filtering and search

---

## Authentication Methods

### Option 1: Token Authentication (Recommended)
1. Call login endpoint to get token
2. Include token in all requests:
   ```
   Authorization: Token <your-token>
   ```

### Option 2: Session Authentication
1. Login through the web interface
2. Cookies are automatically included in requests

---

## Testing API Endpoints

### Using cURL

#### 1. Register Vendor User
```bash
curl -X POST http://localhost:8000/api/vendor/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "vendor1",
    "email": "vendor1@example.com",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

#### 2. Login to Get Token
```bash
curl -X POST http://localhost:8000/api/vendor/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "vendor1",
    "password": "password123"
  }'
```

Save the token from response

#### 3. Submit Vendor Details
```bash
curl -X POST http://localhost:8000/api/vendor/vendor/details/ \
  -H "Authorization: Token <your-token>" \
  -F "shop_name=My Shop" \
  -F "shop_description=Online retail store" \
  -F "address=123 Main St, City" \
  -F "business_type=retail" \
  -F "id_type=gst" \
  -F "id_number=18AABCU9067N1Z5" \
  -F "id_proof_file=@/path/to/file.pdf"
```

#### 4. Get Dashboard
```bash
curl -X GET http://localhost:8000/api/vendor/vendor/dashboard/ \
  -H "Authorization: Token <your-token>"
```

#### 5. List Products
```bash
curl -X GET http://localhost:8000/api/vendor/products/ \
  -H "Authorization: Token <your-token>"
```

#### 6. Create Product
```bash
curl -X POST http://localhost:8000/api/vendor/products/ \
  -H "Authorization: Token <your-token>" \
  -F "name=Product Name" \
  -F "description=Product description" \
  -F "price=99.99" \
  -F "quantity=50" \
  -F "status=pending" \
  -F "image=@/path/to/image.jpg"
```

---

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000/api"

# 1. Register
response = requests.post(f"{BASE_URL}/vendor/register/", json={
    "username": "vendor1",
    "email": "vendor1@example.com",
    "password": "password123",
    "confirm_password": "password123"
})
print(response.json())

# 2. Login
response = requests.post(f"{BASE_URL}/vendor/login/", json={
    "username": "vendor1",
    "password": "password123"
})
token = response.json()["token"]

# 3. Headers with token
headers = {"Authorization": f"Token {token}"}

# 4. Get dashboard
response = requests.get(f"{BASE_URL}/vendor/vendor/dashboard/", headers=headers)
print(response.json())

# 5. List products
response = requests.get(f"{BASE_URL}/vendor/products/", headers=headers)
print(response.json())

# 6. Create product
files = {
    'image': open('/path/to/image.jpg', 'rb')
}
data = {
    'name': 'Product Name',
    'description': 'Product description',
    'price': '99.99',
    'quantity': '50',
    'status': 'pending'
}
response = requests.post(f"{BASE_URL}/vendor/products/", 
                        headers=headers, 
                        files=files, 
                        data=data)
print(response.json())

# 7. Get approval status
response = requests.get(f"{BASE_URL}/vendor/vendor/approval-status/", headers=headers)
print(response.json())
```

---

### Using Postman

1. **Import Collection:**
   - Open Postman
   - Click "Import" → "Upload Files"
   - Select `Ecommerce_API.postman_collection.json`

2. **Set Environment Variables:**
   - Click on the environment dropdown
   - Set `base_url` = `http://localhost:8000/api`
   - After login, set `token` = `<received-token>`

3. **Run Requests:**
   - Use the pre-configured request templates
   - Modify variables as needed

---

## Admin Testing

### Create Admin User
```bash
python manage.py createsuperuser
```

### Get Admin Token
```bash
curl -X POST http://localhost:8000/api/auth/token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_username",
    "password": "admin_password"
  }'
```

### List Vendor Requests
```bash
curl -X GET http://localhost:8000/api/admin/vendor-requests/ \
  -H "Authorization: Token <admin-token>"
```

### Approve Vendor
```bash
curl -X POST http://localhost:8000/api/admin/vendor-requests/1/approve/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "Documents verified"}'
```

### Get Admin Dashboard
```bash
curl -X GET http://localhost:8000/api/admin/dashboard/ \
  -H "Authorization: Token <admin-token>"
```

---

## Common Errors and Solutions

### 401 Unauthorized
**Problem:** "Authentication credentials were not provided"
**Solution:** Include the authorization token in request header:
```
Authorization: Token <your-token>
```

### 400 Bad Request
**Problem:** Invalid field values
**Solution:** Check field values against documentation and ensure:
- All required fields are provided
- Field values match expected types
- File uploads use correct multipart/form-data

### 403 Forbidden
**Problem:** "You do not have permission to perform this action"
**Solution:** Ensure you have the required permissions:
- Vendor endpoints require IsAuthenticated
- Admin endpoints require IsAdminUser
- Make sure you're using the correct user type

### 404 Not Found
**Problem:** Resource not found
**Solution:** Verify the resource ID exists and is correct

### 405 Method Not Allowed
**Problem:** Wrong HTTP method used
**Solution:** Check documentation for correct method (GET, POST, PUT, DELETE)

---

## API Response Format

All successful responses follow this format:

### Success Response (200, 201)
```json
{
  "message": "Operation successful",
  "data": {...}
}
```

or for lists:
```json
[
  {...},
  {...}
]
```

### Error Response (400, 401, 403, 404, 500)
```json
{
  "error": "Error description"
}
```

---

## Frontend Integration

### React Example
```javascript
const BASE_URL = "http://localhost:8000/api";

// Register vendor
const registerVendor = async (credentials) => {
  const response = await fetch(`${BASE_URL}/vendor/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials)
  });
  return response.json();
};

// Login
const loginVendor = async (credentials) => {
  const response = await fetch(`${BASE_URL}/vendor/login/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials)
  });
  const data = await response.json();
  localStorage.setItem("token", data.token);
  return data;
};

// Get dashboard with token
const getDashboard = async () => {
  const token = localStorage.getItem("token");
  const response = await fetch(`${BASE_URL}/vendor/vendor/dashboard/`, {
    method: "GET",
    headers: { "Authorization": `Token ${token}` }
  });
  return response.json();
};
```

### Vue.js Example
```javascript
import axios from 'axios';

const API = axios.create({
  baseURL: "http://localhost:8000/api"
});

// Register
API.post("/vendor/register/", {
  username: "vendor1",
  email: "vendor@example.com",
  password: "password123",
  confirm_password: "password123"
});

// Login and save token
const loginResponse = await API.post("/vendor/login/", {
  username: "vendor1",
  password: "password123"
});
localStorage.setItem("token", loginResponse.data.token);

// Set token in headers for future requests
API.defaults.headers.common["Authorization"] = `Token ${localStorage.getItem("token")}`;

// Get dashboard
API.get("/vendor/vendor/dashboard/");
```

---

## Database Models

### VendorProfile
- id
- user (OneToOneField)
- shop_name
- shop_description
- address
- business_type (retail, wholesale, manufacturer, service)
- id_type (gst, pan)
- id_number
- id_proof_file
- approval_status (pending, approved, rejected)
- rejection_reason
- is_blocked
- blocked_reason
- created_at
- updated_at

### Product
- id
- vendor (ForeignKey to VendorProfile)
- name
- description
- price
- quantity
- image
- status (pending, approved, rejected)
- is_blocked
- blocked_reason
- created_at
- updated_at

### VendorApprovalLog
- id
- vendor (ForeignKey)
- admin_user (ForeignKey)
- action
- reason
- timestamp

### ProductApprovalLog
- id
- product (ForeignKey)
- admin_user (ForeignKey)
- action
- reason
- timestamp

---

## Available Filters and Search

### Vendor List
```
GET /api/vendor/products/?status=approved&search=laptop
```

### Product List
```
GET /api/admin/products/?status=approved&blocked=false&search=phone&vendor_id=1
```

### Vendor Requests
```
GET /api/admin/vendor-requests/?search=shop_name
```

---

## CORS Configuration

API is configured to accept requests from:
- http://localhost:3000
- http://localhost:8080
- http://127.0.0.1:3000
- http://127.0.0.1:8080

To add more origins, edit settings.py:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8080",
    "https://yourdomain.com",  # Add your domain
]
```

---

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use: `netstat -ano | findstr :8000`
- Kill the process: `taskkill /PID <PID> /F`
- Or use different port: `python manage.py runserver 8001`

### Database errors
- Reset database: `python manage.py migrate --fake ecommapp zero` then `python manage.py migrate`
- Or delete db.sqlite3 and run migrations fresh

### Import errors
- Install missing packages: `pip install -r requirements.txt`
- Check Python version: Python 3.8+

### CORS errors
- Verify frontend URL is in CORS_ALLOWED_ORIGINS
- Check that requests include correct headers

---

## Next Steps

1. Start the development server
2. Test endpoints using Postman or cURL
3. Integrate with your frontend application
4. Deploy to production (refer to Django deployment guide)
