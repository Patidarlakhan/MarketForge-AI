/**
 * AI Marketing Content Engine — API Client
 *
 * Base HTTP client for communicating with the FastAPI backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

interface RequestOptions {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
}

/**
 * Make an API request to the backend.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = 'GET', body, headers = {} } = options;

  const config: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  };

  if (body !== undefined) {
    config.body = JSON.stringify(body);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: 'An error occurred' }));

    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}
/** GET request */
export function get<T>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint);
}

/** POST request */
export function post<T>(endpoint: string, body?: unknown): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'POST', body });
}

/** PATCH request */
export function patch<T>(endpoint: string, body: unknown): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PATCH', body });
}

/** PUT request */
export function put<T>(endpoint: string, body: unknown): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'PUT', body });
}

/** DELETE request */
export function del<T>(endpoint: string): Promise<T> {
  return apiRequest<T>(endpoint, { method: 'DELETE' });
}

export default { get, post, put, patch, del };
