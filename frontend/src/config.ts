const inferApiBaseUrl = () => {
  if (import.meta.env.VITE_API_BASE_URL) return import.meta.env.VITE_API_BASE_URL;

  if (typeof window !== 'undefined' && window.location.hostname === 'localhost') {
    return 'http://localhost:8000/api';
  }

  // When running inside Docker, the backend is reachable via its service name
  return 'http://backend:8000/api';
};

export const API_BASE_URL = inferApiBaseUrl();
