import { Bot, LogIn, UserPlus } from "lucide-react";
import { FormEvent, useState } from "react";

import {
  getCurrentUser,
  loginUser,
  registerUser,
  type AuthTokens,
  type User,
} from "../services/api";

type AuthPageProps = {
  mode: "login" | "register";
  onModeChange: (mode: "login" | "register") => void;
  onAuthenticated: (tokens: AuthTokens, user: User) => void;
};

export function AuthPage({ mode, onModeChange, onAuthenticated }: AuthPageProps) {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isRegister = mode === "register";

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setIsSubmitting(true);

    try {
      if (isRegister) {
        await registerUser({
          email,
          username,
          full_name: fullName,
          password,
        });
      }

      const tokens = await loginUser({ email, password });
      localStorage.setItem("access_token", tokens.access_token);
      localStorage.setItem("refresh_token", tokens.refresh_token);
      const user = await getCurrentUser();
      onAuthenticated(tokens, user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Authentication failed");
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="auth-shell">
      <section className="auth-hero">
        <div className="brand auth-brand">
          <Bot size={32} aria-hidden="true" />
          <div>
            <strong>Enterprise AI</strong>
            <span>Copilot Platform</span>
          </div>
        </div>
        <div>
          <p className="eyebrow">Phase 2</p>
          <h1>Secure access for enterprise AI workspaces</h1>
          <p>
            Authentication, role-based access, and governed platform entry are now part of
            the product foundation.
          </p>
        </div>
      </section>

      <section className="auth-panel" aria-label={isRegister ? "Register" : "Login"}>
        <div className="auth-tabs" role="tablist">
          <button
            className={!isRegister ? "active" : ""}
            type="button"
            onClick={() => onModeChange("login")}
          >
            <LogIn size={18} aria-hidden="true" />
            Login
          </button>
          <button
            className={isRegister ? "active" : ""}
            type="button"
            onClick={() => onModeChange("register")}
          >
            <UserPlus size={18} aria-hidden="true" />
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          {isRegister && (
            <>
              <label>
                Full name
                <input
                  autoComplete="name"
                  minLength={2}
                  required
                  type="text"
                  value={fullName}
                  onChange={(event) => setFullName(event.target.value)}
                />
              </label>
              <label>
                Username
                <input
                  autoComplete="username"
                  minLength={3}
                  pattern="[a-zA-Z0-9_.-]+"
                  required
                  type="text"
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                />
              </label>
            </>
          )}

          <label>
            Email
            <input
              autoComplete="email"
              required
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
            />
          </label>

          <label>
            Password
            <input
              autoComplete={isRegister ? "new-password" : "current-password"}
              minLength={8}
              required
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>

          {error && <p className="form-error">{error}</p>}

          <button className="submit-button" disabled={isSubmitting} type="submit">
            {isSubmitting ? "Please wait..." : isRegister ? "Create Account" : "Login"}
          </button>
        </form>
      </section>
    </main>
  );
}
