# Frontend API Integration Guide

## Base URL
- **Local**: `http://localhost:8000`
- **Production**: `https://jobpromax-manager-be-2.onrender.com`

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
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Generic fetch wrapper
async function apiFetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    credentials: 'include', // REQUIRED for cookies
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!res.ok) {
    const error = await res.json();
    throw new Error(error.detail || 'API Error');
  }
  
  return res.json();
}
```

---

## Frontend Implementation Examples

### 1. Auth Service
```typescript
// services/auth.ts
interface User {
  id: string;
  name: string;
  email: string;
  role: 'manager' | 'developer' | 'leadership';
}

interface LoginResponse {
  message: string;
  user: User;
}

export const authService = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    return apiFetch('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  logout: async (): Promise<void> => {
    await apiFetch('/auth/logout', { method: 'POST' });
  },

  getCurrentUser: async (): Promise<User> => {
    return apiFetch('/auth/me');
  },
};
```

### 2. Auth Context (React)
```tsx
// context/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    authService.getCurrentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  const login = async (email: string, password: string) => {
    const { user } = await authService.login(email, password);
    setUser(user);
    return user;
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

### 3. Login Page
```tsx
// pages/login.tsx
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      {error && <p>{error}</p>}
      <button type="submit">Login</button>
    </form>
  );
}
```

### 4. Protected Route Wrapper
```tsx
// components/ProtectedRoute.tsx
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export function ProtectedRoute({ children, allowedRoles = [] }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
    if (!loading && user && allowedRoles.length > 0 && !allowedRoles.includes(user.role)) {
      router.push('/unauthorized');
    }
  }, [user, loading]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  return children;
}
```

### 5. Fetching Protected Data
```typescript
// Example: Fetch tasks
const tasks = await apiFetch('/tasks');

// Example: Update task
await apiFetch(`/tasks/${taskId}`, {
  method: 'PATCH',
  body: JSON.stringify({ status: 'Done' }),
});
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
