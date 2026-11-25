import React, { useState } from 'react';
import {
  Box,
  Lock,
  User,
  Mail,
  ArrowRight,
  Sun,
  Moon,
  ShieldCheck,
  Code2,
  ExternalLink,
  Layers,
  Zap,
  FileCode,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { SAMPLE_CATALOG } from './SampleModal';

export function LoginDashboard() {
  const { login, register, authError, setAuthError } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin');
  const [email, setEmail] = useState('sri.anjaneya.kailash@gmail.com');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) {
      setAuthError('Please enter valid credentials');
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
      // Handled by AuthContext
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-showcase-page">
      {/* Background Ambient Orbs */}
      <div className="ambient-glow-orb ambient-orb-1" />
      <div className="ambient-glow-orb ambient-orb-2" />

      {/* Top Header */}
      <header className="login-top-nav">
        <div className="nav-brand">
          <div className="nav-logo-box">
            <Box className="w-4 h-4 text-slate-200" />
          </div>
          <span className="nav-title">PolyGen</span>
          <span className="nav-tagline">3D Asset Studio</span>
        </div>

        <div className="nav-right-items">
          <a
            href="/viewer/"
            target="_blank"
            rel="noreferrer"
            className="nav-ghost-link"
            title="Physical 3D Assembly Lab"
          >
            <span>Physical Lab</span>
            <ExternalLink className="w-3 h-3 opacity-40" />
          </a>

          <a
            href="/viewer/build.html"
            target="_blank"
            rel="noreferrer"
            className="nav-ghost-link"
            title="Digital Engineering Lab"
          >
            <span>Digital Lab</span>
            <ExternalLink className="w-3 h-3 opacity-40" />
          </a>

          <button
            onClick={toggleTheme}
            className="nav-icon-btn"
            title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
            type="button"
          >
            {theme === 'dark' ? (
              <Sun className="w-3.5 h-3.5 text-amber-400" />
            ) : (
              <Moon className="w-3.5 h-3.5 text-slate-700" />
            )}
          </button>

          <a
            href="https://github.com/Kailash-18/PolyGen"
            target="_blank"
            rel="noreferrer"
            className="nav-icon-btn"
            title="GitHub Repository"
          >
            <Code2 className="w-3.5 h-3.5 text-slate-400" />
          </a>
        </div>
      </header>

      {/* Main Split Showcase Container */}
      <main className="login-split-layout">
        {/* Left Side: Product Greatness & Why to Use PolyGen */}
        <section className="login-hero-showcase">
          <div className="hero-pill-badge">
            <span className="hero-pulse-dot" />
            <span>Generative 3D Asset Pipeline</span>
          </div>

          <h1 className="hero-headline">
            Turn natural language into game-ready 3D assets in seconds.
          </h1>

          <p className="hero-lead">
            PolyGen synthesizes watertight 3D geometry, automatically maps 1024px PBR textures, 
            and optimizes topology using Quadric Error Metrics for direct import into Unreal Engine 5, 
            Unity, and Blender.
          </p>

          {/* 4 Core Pillars: Clean Monochrome / Subtle Slate */}
          <div className="hero-pillars-grid">
            <div className="pillar-card">
              <div className="pillar-icon-box">
                <Box className="w-4 h-4 text-slate-200" />
              </div>
              <div className="pillar-text">
                <h3 className="pillar-title">Manifold 3D Geometry</h3>
                <p className="pillar-desc">
                  Generates recognizable, watertight meshes (weapons, props, vases, furniture) with clean manifold topology.
                </p>
              </div>
            </div>

            <div className="pillar-card">
              <div className="pillar-icon-box">
                <Layers className="w-4 h-4 text-slate-200" />
              </div>
              <div className="pillar-text">
                <h3 className="pillar-title">Automated PBR Texture Maps</h3>
                <p className="pillar-desc">
                  Conformal UV unwrapping with 1024px Albedo, Normal, and Roughness maps baked directly into binary GLB.
                </p>
              </div>
            </div>

            <div className="pillar-card">
              <div className="pillar-icon-box">
                <Zap className="w-4 h-4 text-slate-200" />
              </div>
              <div className="pillar-text">
                <h3 className="pillar-title">QEM Topology Optimization</h3>
                <p className="pillar-desc">
                  Intelligently downsamples 500k-polygon geometry to game targets (~10k) while preserving sharp contours.
                </p>
              </div>
            </div>

            <div className="pillar-card">
              <div className="pillar-icon-box">
                <FileCode className="w-4 h-4 text-slate-200" />
              </div>
              <div className="pillar-text">
                <h3 className="pillar-title">Studio Viewport & Kinematics</h3>
                <p className="pillar-desc">
                  Interactive Three.js studio with clay shading, wireframe mesh inspect, CAD camera angles, and exploded view.
                </p>
              </div>
            </div>
          </div>

          {/* Clean Telemetry Strip */}
          <div className="hero-stats-row">
            <div className="hero-stat-item">
              <span className="hero-stat-value">&lt; 1.0s</span>
              <span className="hero-stat-label">Inference Latency</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat-item">
              <span className="hero-stat-value">10k</span>
              <span className="hero-stat-label">Target Polycount</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat-item">
              <span className="hero-stat-value">100%</span>
              <span className="hero-stat-label">Watertight Manifold</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat-item">
              <span className="hero-stat-value">3 Maps</span>
              <span className="hero-stat-label">PBR Textures</span>
            </div>
          </div>
        </section>

        {/* Right Side: Clean Auth Card (No Demo Buttons) */}
        <section className="login-auth-pane">
          <div className="login-auth-card">
            {/* Header */}
            <div className="auth-card-top">
              <h2 className="auth-card-title">
                {isRegister ? 'Create Account' : 'Sign In'}
              </h2>
              <p className="auth-card-sub">
                {isRegister
                  ? 'Join PolyGen to synthesize and inspect 3D assets'
                  : 'Enter your credentials to launch the 3D studio'}
              </p>
            </div>

            {/* Segmented Sign In / Register Tabs */}
            <div className="auth-mode-switch">
              <button
                type="button"
                onClick={() => {
                  setIsRegister(false);
                  setAuthError(null);
                }}
                className={`auth-switch-btn ${!isRegister ? 'active' : ''}`}
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsRegister(true);
                  setAuthError(null);
                }}
                className={`auth-switch-btn ${isRegister ? 'active' : ''}`}
              >
                Register
              </button>
            </div>

            {/* Error Banner */}
            {authError && (
              <div className="auth-alert-box">
                <span>{authError}</span>
              </div>
            )}

            {/* Credentials Form */}
            <form onSubmit={handleSubmit} className="auth-input-form">
              <div className="auth-field-group">
                <label className="auth-label">Username</label>
                <div className="auth-input-wrapper">
                  <User className="w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Username"
                    autoComplete="username"
                    required
                    className="auth-text-input"
                  />
                </div>
              </div>

              {isRegister && (
                <div className="auth-field-group">
                  <label className="auth-label">Email Address</label>
                  <div className="auth-input-wrapper">
                    <Mail className="w-3.5 h-3.5 text-slate-400" />
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="name@polygen.ai"
                      autoComplete="email"
                      required
                      className="auth-text-input"
                    />
                  </div>
                </div>
              )}

              <div className="auth-field-group">
                <label className="auth-label">Password</label>
                <div className="auth-input-wrapper">
                  <Lock className="w-3.5 h-3.5 text-slate-400" />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    autoComplete="current-password"
                    required
                    className="auth-text-input"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="auth-submit-action"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="clean-spinner" />
                    <span>Loading...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center gap-2">
                    <span>{isRegister ? 'Create Account' : 'Start Studio'}</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </div>
                )}
              </button>
            </form>

            {/* Footer Trust Tag */}
            <div className="auth-card-footer">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
              <span>Infotact Solutions · 3D Generative Pipeline</span>
            </div>
          </div>
        </section>
      </main>

      {/* 3D Animated Samples Showcase: "What can you build with PolyGen?" */}
      <section className="showcase-samples-section">
        <div className="showcase-samples-header">
          <div className="showcase-badge">
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            <span>Interactive 3D Asset Showcase</span>
          </div>
          <h2 className="showcase-section-title">What can you build with PolyGen?</h2>
          <p className="showcase-section-sub">
            From procedural armaments to industrial precision hardware, inspect interactive samples with clean topology and game-ready PBR textures.
          </p>
        </div>

        <div className="samples-track-container">
          <div className="samples-3d-track">
            {[...SAMPLE_CATALOG, ...SAMPLE_CATALOG].map((sample, idx) => (
              <div key={`${sample.id}-${idx}`} className="sample-3d-card group">
                <div className="sample-card-top">
                  <span className="sample-card-icon">{sample.icon}</span>
                  <span className="sample-category-tag">{sample.category}</span>
                </div>
                <h4 className="sample-card-title">{sample.name}</h4>
                <p className="sample-card-prompt">{sample.prompt}</p>

                <div className="sample-card-metrics">
                  <div className="sample-metric">
                    <span className="metric-num">{sample.faces.toLocaleString()}</span>
                    <span className="metric-lbl">Polys</span>
                  </div>
                  <div className="sample-metric">
                    <span className="metric-num">{sample.vertices.toLocaleString()}</span>
                    <span className="metric-lbl">Verts</span>
                  </div>
                  <div className="sample-metric">
                    <span className="metric-num text-emerald-400">{sample.decimation}</span>
                    <span className="metric-lbl">QEM</span>
                  </div>
                </div>

                <div className="sample-card-footer">
                  <div className="sample-maps-chips">
                    {sample.maps.map((m) => (
                      <span key={m} className="sample-map-chip">{m}</span>
                    ))}
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setUsername('admin');
                      setPassword('admin');
                      login('admin', 'admin');
                    }}
                    className="sample-try-btn"
                    title="Launch sample in Studio"
                  >
                    <span>Inspect</span>
                    <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

export default LoginDashboard;