import React, { useState } from 'react';
import {
  Box,
  Lock,
  User,
  Mail,
  ArrowRight,
  Sun,
  Moon,
  Sparkles,
  ShieldCheck,
  Code2,
  ExternalLink
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

export function LoginDashboard() {
  const { login, register, authError, setAuthError } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin');
  const [email, setEmail] = useState('admin@polygen.ai');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setAuthError('Wrong credentials');
      return;
    }

    setIsLoading(true);
    try {
      if (isRegister) {
        await register(username.trim(), password.trim(), email.trim());
      } else {
        await login(username.trim(), password.trim());
      }
    } catch {
      // Error handled by AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuickAdminLogin = async () => {
    setUsername('admin');
    setPassword('admin');
    setIsLoading(true);
    try {
      await login('admin', 'admin');
    } catch {
      // Error handled
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="clean-login-page">
      {/* Top Floating Header */}
      <header className="clean-login-nav">
        <div className="nav-brand">
          <div className="nav-logo">
            <Box className="w-5 h-5 text-purple-400" />
          </div>
          <span className="clean-brand-name">
            Poly<span className="brand-accent">Gen</span>
          </span>
        </div>

        <div className="clean-nav-links">
          <a
            href="/viewer/"
            target="_blank"
            rel="noreferrer"
            className="clean-text-link"
          >
            <span>Physical Lab</span>
            <ExternalLink className="w-3 h-3 opacity-60" />
          </a>

          <a
            href="/viewer/build.html"
            target="_blank"
            rel="noreferrer"
            className="clean-text-link"
          >
            <span>Digital Lab</span>
            <ExternalLink className="w-3 h-3 opacity-60" />
          </a>

          <button
            onClick={toggleTheme}
            className="clean-icon-btn"
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            type="button"
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4 text-amber-400" />
            ) : (
              <Moon className="w-4 h-4 text-purple-600" />
            )}
          </button>

          <a
            href="https://github.com/Kailash-18/PolyGen"
            target="_blank"
            rel="noreferrer"
            className="clean-icon-btn"
            title="GitHub Repository"
          >
            <Code2 className="w-4 h-4" />
          </a>
        </div>
      </header>

      {/* Main Minimalist Auth Card */}
      <main className="clean-auth-container">
        <div className="clean-auth-card">
          {/* Card Header */}
          <div className="clean-auth-header">
            <div className="clean-badge">
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span>3D Generative Pipeline</span>
            </div>
            <h1 className="clean-title">
              {isRegister ? 'Create an account' : 'Welcome back'}
            </h1>
            <p className="clean-subtitle">
              {isRegister
                ? 'Sign up to generate and inspect 3D game-ready assets'
                : 'Sign in to access your 3D Studio & Asset Library'}
            </p>
          </div>

          {/* Clean Segmented Tab Switcher */}
          <div className="clean-tab-group">
            <button
              type="button"
              onClick={() => {
                setIsRegister(false);
                setAuthError(null);
              }}
              className={`clean-tab-btn ${!isRegister ? 'active' : ''}`}
            >
              Sign In
            </button>
            <button
              type="button"
              onClick={() => {
                setIsRegister(true);
                setAuthError(null);
              }}
              className={`clean-tab-btn ${isRegister ? 'active' : ''}`}
            >
              Register
            </button>
          </div>

          {/* Quick Demo Access Bar */}
          {!isRegister && (
            <button
              type="button"
              onClick={handleQuickAdminLogin}
              className="clean-demo-bar"
              disabled={isLoading}
            >
              <span className="clean-demo-dot" />
              <span className="clean-demo-text">Quick Demo: <b>admin / admin</b></span>
              <ArrowRight className="w-3.5 h-3.5 opacity-60 ml-auto" />
            </button>
          )}

          {/* Error Message */}
          {authError && (
            <div className="clean-error-alert">
              <span>{authError}</span>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="clean-form">
            <div className="clean-field">
              <label>Username</label>
              <div className="clean-input-box">
                <User className="w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="admin"
                  autoComplete="off"
                  required
                />
              </div>
            </div>

            {isRegister && (
              <div className="clean-field">
                <label>Email Address</label>
                <div className="clean-input-box">
                  <Mail className="w-4 h-4 text-slate-400" />
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="admin@polygen.ai"
                    autoComplete="off"
                    required
                  />
                </div>
              </div>
            )}

            <div className="clean-field">
              <label>Password</label>
              <div className="clean-input-box">
                <Lock className="w-4 h-4 text-slate-400" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  autoComplete="off"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="clean-submit-btn"
            >
              {isLoading ? (
                <div className="clean-spinner-row">
                  <div className="clean-spinner" />
                  <span>Signing In...</span>
                </div>
              ) : (
                <div className="clean-spinner-row">
                  <span>{isRegister ? 'Create Account' : 'Enter Studio'}</span>
                  <ArrowRight className="w-4 h-4" />
                </div>
              )}
            </button>
          </form>

          {/* Security Tagline */}
          <div className="clean-footer-tag">
            <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            <span>Infotact Solutions · 3D Generative Pipeline</span>
          </div>
        </div>
      </main>
    </div>
  );
}
