// Amplify's build replaces this placeholder with the API_BASE env var (see amplify.yml)
const DEPLOYED_API = '__API_BASE__';

// Local dev talks to uvicorn; otherwise the Amplify-injected URL, else the Render backend
const API = ['localhost', '127.0.0.1'].includes(location.hostname)
  ? 'http://localhost:8000/api'
  : DEPLOYED_API.startsWith('http') ? DEPLOYED_API : 'https://evently-api.onrender.com/api';

function token() {
  return localStorage.getItem('token');
}

async function api(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token()) {
    headers.Authorization = `Bearer ${token()}`;
  }

  const res = await fetch(API + path, {
    ...options,
    headers
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || 'Request failed');
  }

  return data;
}

function logout() {
  localStorage.removeItem('token');
  location.href = 'login.html';
}