# Frontend API Integration Guide

## Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://your-render-url.onrender.com`

## Authentication

### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "manager@jobpromax.com",
  "password": "manager123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "user": {
    "id": "675...",
    "name": "Manager User",
    "email": "manager@jobpromax.com",
    "role": "manager"
  }
}
```
> **Cookie**: `auth-token` (HttpOnly) is set automatically.

### Logout
```http
POST /auth/logout
```

### Get Current User
```http
GET /auth/me
```
**Response (200):**
```json
{
  "id": "675...",
  "name": "Manager User",
  "email": "manager@jobpromax.com",
  "role": "manager"
}
```

---

## Frontend Fetch Configuration

Since auth uses **HTTP-only cookies**, include `credentials: 'include'` in all requests:

```typescript
// Example: Login
const login = async (email: string, password: string) => {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',  // REQUIRED for cookies
    body: JSON.stringify({ email, password })
  });
  return res.json();
};

// Example: Fetch protected data
const getTasks = async () => {
  const res = await fetch(`${API_BASE}/tasks`, {
    credentials: 'include'  // REQUIRED
  });
  return res.json();
};
```

---

## Protected Endpoints (Require Auth Cookie)

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks |
| PATCH | `/tasks/{id}` | Update a task |

### Roadmap
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/roadmap` | List phases |
| POST | `/roadmap` | Create phase |
| PATCH | `/roadmap/{id}` | Update phase |
| DELETE | `/roadmap/{id}` | Delete phase |

### Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/features` | List features |
| POST | `/features` | Create feature |
| PATCH | `/features/{id}` | Update feature |
| DELETE | `/features/{id}` | Delete feature |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/dashboard/kpi` | Get KPIs |
| GET | `/pipeline` | Get pipeline items |
| GET | `/dashboard/charts/burnup` | Burnup chart data |
| GET | `/dashboard/charts/velocity` | Velocity chart data |

---

## User Management (Manager Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List all users |
| POST | `/users/` | Create user |
| DELETE | `/users/{id}` | Delete user |

**Create User Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "developer",
  "password": "tempPassword123"
}
```
> Roles: `manager`, `developer`, `leadership`

---

## CORS Configuration

Backend allows:
- Origin: `http://localhost:3000` (dev)
- Credentials: `true`

Update `ALLOWED_ORIGINS` in `.env` for production frontend URL.

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 401 | Not authenticated (missing/invalid cookie) |
| 403 | Forbidden (insufficient role) |
| 404 | Resource not found |
| 422 | Validation error |
