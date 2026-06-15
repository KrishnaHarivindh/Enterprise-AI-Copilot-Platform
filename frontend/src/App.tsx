import { useEffect, useState } from "react";

import { AuthPage } from "./pages/AuthPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { getCurrentUser, type AuthTokens, type User } from "./services/api";

type AuthMode = "login" | "register";

export default function App() {
  const [user, setUser] = useState<User | null>(null);
  const [authMode, setAuthMode] = useState<AuthMode>("login");
  const [isLoading, setIsLoading] = useState(true);
  const [activePage, setActivePage] = useState("Dashboard");

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setIsLoading(false);
      return;
    }

    getCurrentUser()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
      })
      .finally(() => setIsLoading(false));
  }, []);

  function handleAuthenticated(tokens: AuthTokens, authenticatedUser: User) {
    localStorage.setItem("access_token", tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
    setUser(authenticatedUser);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setUser(null);
    setAuthMode("login");
  }

  if (isLoading) {
    return <div className="loading-screen">Loading workspace...</div>;
  }

  if (!user) {
    return (
      <AuthPage
        mode={authMode}
        onModeChange={setAuthMode}
        onAuthenticated={handleAuthenticated}
      />
    );
  }

  if (activePage === "Documents") {
    return (
      <DocumentsPage
        activePage={activePage}
        user={user}
        onLogout={handleLogout}
        onNavigate={setActivePage}
      />
    );
  }

  return (
    <DashboardPage
      activePage={activePage}
      user={user}
      onLogout={handleLogout}
      onNavigate={setActivePage}
    />
  );
}
