import {
  Activity,
  Database,
  FileText,
  Settings,
  ShieldCheck,
  Users,
  Workflow,
} from "lucide-react";

import { AppSidebar } from "../components/AppSidebar";
import { MetricCard } from "../components/MetricCard";
import type { User } from "../services/api";

const capabilities = [
  {
    title: "RAG Knowledge Base",
    description: "Document ingestion, embeddings, semantic search, and cited answers.",
    icon: FileText,
  },
  {
    title: "Agent Workflows",
    description: "Specialized assistants for reports, summaries, analysis, and operations.",
    icon: Workflow,
  },
  {
    title: "Governed Access",
    description: "Role-aware platform foundation for admins, managers, and employees.",
    icon: ShieldCheck,
  },
];

type DashboardPageProps = {
  activePage: string;
  user: User;
  onLogout: () => void;
  onNavigate: (page: string) => void;
};

export function DashboardPage({ activePage, user, onLogout, onNavigate }: DashboardPageProps) {
  return (
    <main className="app-shell">
      <AppSidebar activePage={activePage} user={user} onLogout={onLogout} onNavigate={onNavigate} />

      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Phase 3.1 Document Management</p>
            <h1>Welcome {user.full_name}</h1>
            <p className="role-line">Role: {user.role}</p>
          </div>
          <button type="button">
            <Settings size={18} aria-hidden="true" />
            Workspace Settings
          </button>
        </header>

        <section className="metrics" aria-label="Platform metrics">
          <MetricCard label="Documents Indexed" value="0" icon={Database} />
          <MetricCard label="Queries Run" value="0" icon={Activity} />
          <MetricCard label="Agents Available" value="0" icon={Workflow} />
        </section>

        <section className="content-grid">
          <div className="panel primary-panel">
            <div>
              <p className="eyebrow">AI-Ready Foundation</p>
              <h2>Documents are now the enterprise knowledge boundary</h2>
              <p>
                Upload, metadata indexing, ownership checks, text extraction, lifecycle
                controls, and audit logs prepare the platform for vector search and RAG.
              </p>
            </div>
            <div className="status-list">
              <span>Secure file upload</span>
              <span>Metadata indexing</span>
              <span>Text extraction pipeline</span>
              <span>Audit log tracking</span>
            </div>
          </div>

          <div className="panel">
            <h2>Access Summary</h2>
            <article className="identity-card">
              <Users size={24} aria-hidden="true" />
              <div>
                <strong>{user.full_name}</strong>
                <span>{user.email}</span>
              </div>
            </article>
            <div className="capability-list">
              {capabilities.map((item) => (
                <article className="capability" key={item.title}>
                  <item.icon size={22} aria-hidden="true" />
                  <div>
                    <h3>{item.title}</h3>
                    <p>{item.description}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}
