import { Bot, LogOut } from "lucide-react";

import type { User } from "../services/api";

type AppSidebarProps = {
  activePage: string;
  user: User;
  onNavigate: (page: string) => void;
  onLogout: () => void;
};

export function AppSidebar({ activePage, user, onNavigate, onLogout }: AppSidebarProps) {
  const navItems = ["Dashboard", "Documents", "AI Agents", "Analytics", "Settings"];
  const visibleNavItems = user.role === "ADMIN" ? [...navItems, "Admin"] : navItems;

  return (
    <aside className="sidebar">
      <div className="brand">
        <Bot size={28} aria-hidden="true" />
        <div>
          <strong>Enterprise AI</strong>
          <span>Copilot Platform</span>
        </div>
      </div>

      <nav aria-label="Primary navigation">
        {visibleNavItems.map((item) => (
          <button
            className={activePage === item ? "active" : ""}
            key={item}
            type="button"
            onClick={() => onNavigate(item)}
          >
            {item}
          </button>
        ))}
      </nav>

      <button className="logout-button" type="button" onClick={onLogout}>
        <LogOut size={18} aria-hidden="true" />
        Logout
      </button>
    </aside>
  );
}
