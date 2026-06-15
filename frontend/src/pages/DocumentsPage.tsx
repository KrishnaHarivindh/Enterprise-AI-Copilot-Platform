import { Download, FileText, Search, Trash2, UploadCloud } from "lucide-react";
import { ChangeEvent, DragEvent, useEffect, useMemo, useState } from "react";

import { AppSidebar } from "../components/AppSidebar";
import {
  deleteDocument,
  getDocumentDownloadUrl,
  listAuditLogs,
  listDocuments,
  uploadDocument,
  type AuditLogRecord,
  type DocumentRecord,
  type User,
} from "../services/api";

type DocumentsPageProps = {
  activePage: string;
  user: User;
  onLogout: () => void;
  onNavigate: (page: string) => void;
};

const allowedExtensions = [".pdf", ".docx", ".txt", ".csv", ".md"];

export function DocumentsPage({ activePage, user, onLogout, onNavigate }: DocumentsPageProps) {
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [activity, setActivity] = useState<AuditLogRecord[]>([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const totalSize = useMemo(
    () => documents.reduce((sum, document) => sum + document.size_bytes, 0),
    [documents],
  );

  useEffect(() => {
    refreshDocuments();
  }, []);

  async function refreshDocuments(query = search) {
    setIsLoading(true);
    setError("");
    try {
      const [documentData, auditData] = await Promise.all([listDocuments(query), listAuditLogs()]);
      setDocuments(documentData);
      setActivity(auditData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load documents");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleFile(file: File | undefined) {
    if (!file) return;
    const hasAllowedExtension = allowedExtensions.some((extension) =>
      file.name.toLowerCase().endsWith(extension),
    );

    if (!hasAllowedExtension) {
      setError(`Unsupported file type. Allowed: ${allowedExtensions.join(", ")}`);
      return;
    }

    setIsUploading(true);
    setError("");
    try {
      await uploadDocument(file);
      await refreshDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setIsUploading(false);
    }
  }

  function handleInputChange(event: ChangeEvent<HTMLInputElement>) {
    handleFile(event.target.files?.[0]);
    event.target.value = "";
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    handleFile(event.dataTransfer.files[0]);
  }

  async function handleDelete(documentId: string) {
    setError("");
    try {
      await deleteDocument(documentId);
      await refreshDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Delete failed");
    }
  }

  function handleSearchSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    refreshDocuments(search);
  }

  return (
    <main className="app-shell">
      <AppSidebar activePage={activePage} user={user} onLogout={onLogout} onNavigate={onNavigate} />

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Document Management</p>
            <h1>Enterprise Knowledge Files</h1>
          </div>
        </header>

        <section className="metrics" aria-label="Document metrics">
          <article className="metric-card">
            <FileText size={22} aria-hidden="true" />
            <div>
              <span>Total Documents</span>
              <strong>{documents.length}</strong>
            </div>
          </article>
          <article className="metric-card">
            <UploadCloud size={22} aria-hidden="true" />
            <div>
              <span>Storage Used</span>
              <strong>{formatBytes(totalSize)}</strong>
            </div>
          </article>
          <article className="metric-card">
            <Search size={22} aria-hidden="true" />
            <div>
              <span>Search Mode</span>
              <strong>Keyword</strong>
            </div>
          </article>
        </section>

        <section className="documents-layout">
          <div className="panel">
            <label
              className="upload-zone"
              onDragOver={(event) => event.preventDefault()}
              onDrop={handleDrop}
            >
              <UploadCloud size={28} aria-hidden="true" />
              <strong>{isUploading ? "Uploading..." : "Upload document"}</strong>
              <span>PDF, DOCX, TXT, CSV, or MD up to 10 MB</span>
              <input
                accept={allowedExtensions.join(",")}
                disabled={isUploading}
                type="file"
                onChange={handleInputChange}
              />
            </label>

            <form className="search-row" onSubmit={handleSearchSubmit}>
              <input
                placeholder="Search filenames or extracted text"
                type="search"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
              <button type="submit">
                <Search size={18} aria-hidden="true" />
                Search
              </button>
            </form>

            {error && <p className="form-error">{error}</p>}

            <div className="table-shell">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Version</th>
                    <th>Size</th>
                    <th>Status</th>
                    <th>Upload Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((document) => (
                    <tr key={document.id}>
                      <td>{document.original_filename}</td>
                      <td>{document.file_type.toUpperCase()}</td>
                      <td>v{document.version_number}</td>
                      <td>{formatBytes(document.size_bytes)}</td>
                      <td>
                        <span className={`status-pill ${document.status.toLowerCase()}`}>
                          {document.status}
                        </span>
                      </td>
                      <td>{new Date(document.created_at).toLocaleDateString()}</td>
                      <td>
                        <div className="action-row">
                          <a
                            className="icon-action"
                            href={getDocumentDownloadUrl(document.id)}
                            rel="noreferrer"
                            target="_blank"
                            title="Download document"
                          >
                            <Download size={17} aria-hidden="true" />
                          </a>
                          <button
                            className="icon-action danger"
                            title="Delete document"
                            type="button"
                            onClick={() => handleDelete(document.id)}
                          >
                            <Trash2 size={17} aria-hidden="true" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                  {!isLoading && documents.length === 0 && (
                    <tr>
                      <td colSpan={7}>No documents uploaded yet.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <aside className="panel activity-panel">
            <h2>Activity Feed</h2>
            <div className="activity-list">
              {activity.map((item) => (
                <article key={item.id}>
                  <strong>{item.description}</strong>
                  <span>{new Date(item.created_at).toLocaleString()}</span>
                </article>
              ))}
              {!isLoading && activity.length === 0 && <p>No activity yet.</p>}
            </div>
          </aside>
        </section>
      </section>
    </main>
  );
}

function formatBytes(bytes: number) {
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const index = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), units.length - 1);
  return `${(bytes / 1024 ** index).toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}
