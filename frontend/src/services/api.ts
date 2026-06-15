const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export type UserRole = "ADMIN" | "MANAGER" | "EMPLOYEE";

export type User = {
  id: string;
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type AuthTokens = {
  access_token: string;
  refresh_token: string;
  token_type: "bearer";
};

export type RegisterPayload = {
  email: string;
  username: string;
  full_name: string;
  password: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type DocumentRecord = {
  id: string;
  filename: string;
  original_filename: string;
  file_type: string;
  mime_type: string;
  size_bytes: number;
  owner_id: string;
  parent_document_id: string | null;
  version_number: number;
  status: "UPLOADED" | "PROCESSED" | "FAILED";
  chunk_count: number;
  embedding_status: "PENDING" | "READY" | "FAILED";
  created_at: string;
  updated_at: string;
};

export type AuditLogRecord = {
  id: string;
  actor_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  description: string;
  created_at: string;
};

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers = new Headers(options.headers);

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(data?.detail ?? "Request failed");
  }

  return data as T;
}

export async function getHealth() {
  return request("/health");
}

export async function registerUser(payload: RegisterPayload) {
  return request<User>("/auth/register", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function loginUser(payload: LoginPayload) {
  return request<AuthTokens>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getCurrentUser() {
  return request<User>("/auth/me");
}

export async function listUsers() {
  return request<User[]>("/users");
}

export async function listDocuments(search = "") {
  const query = search ? `?search=${encodeURIComponent(search)}` : "";
  return request<DocumentRecord[]>(`/documents${query}`);
}

export async function uploadDocument(file: File) {
  const body = new FormData();
  body.append("file", file);
  return request<DocumentRecord>("/documents/upload", {
    method: "POST",
    body,
  });
}

export async function deleteDocument(documentId: string) {
  await request<null>(`/documents/${documentId}`, {
    method: "DELETE",
  });
}

export function getDocumentDownloadUrl(documentId: string) {
  return `${API_BASE_URL}/documents/${documentId}/download`;
}

export async function listAuditLogs() {
  return request<AuditLogRecord[]>("/audit-logs");
}
