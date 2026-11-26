import React, { useState } from 'react';
import {
  Sparkles,
  ArrowRight,
  Sun,
  Moon,
  Code2,
  Lock,
  User,
  Mail,
  Zap,
  ShieldCheck,
  ChevronDown,
  Box,
  Layers
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Login3DScene } from '../canvas/Login3DScene';

const MODEL_PRESETS = [
  { id: 'core', label: 'Quantum Core', icon: '⚛️' },
  { id: 'car', label: 'Cyber Car', icon: '🏎️' },
  { id: 'mech', label: 'Titan Mech', icon: '🤖' },
  { id: 'blade', label: 'Plasma Blade', icon: '⚔️' },
  { id: 'vase', label: 'Sacred Urn', icon: '🏺' }
];

const SUGGESTED_PROMPTS = [
  'A round wooden dining table with four carved legs',
  'A medieval castle tower with stone battlements',
  'A cybernetic robotic arm with gripper claw',
  'An ancient pirate rum barrel with iron rings',
  'A high-tech sci-fi plasma cannon turret'
];

export function LoginDashboard() {
  const { login, register, loginAsGuest, authError, setAuthError } = useAuth();
  const { theme, toggleTheme } = useTheme();

  const [activeModel, setActiveModel] = useState<string>('core');
  const [promptInput, setPromptInput] = useState<string>('A round wooden dining table with four carved legs');
  const [showAuthForm, setShowAuthForm] = useState<boolean>(false);
  const [isRegister, setIsRegister] = useState(false);
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin');
  const [email, setEmail] = useState('sri.anjaneya.kailash@gmail.com');
  const [isLoading, setIsLoading] = useState(false);

  const handleLaunchWithPrompt = (e: React.FormEvent) => {
    e.preventDefault();
    if (promptInput.trim()) {
      localStorage.setItem('polygen_pending_prompt', promptInput.trim());
    }
    loginAsGuest();
  };

  const handleSelectSuggestion = (p: string) => {
    setPromptInput(p);
  };

  const handleAuthSubmit = async (e: React.FormEvent) => {
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
    <div className="login-3d-universe">
      {/* Living Interactive 3D WebGL Scene */}
      <Login3DScene activeModel={activeModel} />

      {/* Top Floating Glass Header */}
      <header className="login-floating-nav">
        <div className="nav-brand-capsule">
          <svg className="vre-mark w-7 h-7 flex-shrink-0" viewBox="0 0 32 32" aria-hidden="true">
            <path className="m3" d="M16 20.5 27 25.5 16 30.5 5 25.5Z" fill="#8b7bff" fillOpacity=".85" />
            <path className="m2" d="M16 11.5 27 16.5 16 21.5 5 16.5Z" fill="#4f8cff" fillOpacity=".9" />
            <path className="m1" d="M16 2.5 27 7.5 16 12.5 5 7.5Z" fill="#5ee6ff" />
          </svg>
          <div className="nav-brand-text">
            <span className="nav-brand-title">PolyGen 3D</span>
            <span className="nav-brand-subtitle">Text-to-3D AI Studio</span>
          </div>
        </div>

        {/* 3D Model Switcher Pills */}
        <div className="model-switcher-bar">
          {MODEL_PRESETS.map((m) => (
            <button
              key={m.id}
              type="button"
              onClick={() => setActiveModel(m.id)}
              className={`model-pill-btn ${activeModel === m.id ? 'active' : ''}`}
            >
              <span>{m.icon}</span>
              <span className="hidden sm:inline">{m.label}</span>
            </button>
          ))}
        </div>

        {/* Right Action Icons */}
        <div className="nav-right-actions">
          <button
            type="button"
            onClick={loginAsGuest}
            className="nav-quick-launch-btn"
            title="Instant 3D Studio Access"
          >
            <Sparkles className="w-3.5 h-3.5 text-cyan-300" />
            <span>Launch Studio</span>
            <ArrowRight className="w-3.5 h-3.5 text-cyan-300" />
          </button>

          <button
            onClick={toggleTheme}
            className="nav-glass-icon-btn"
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
            className="nav-glass-icon-btn"
            title="GitHub Repository"
          >
            <Code2 className="w-3.5 h-3.5 text-slate-400" />
          </a>
        </div>
      </header>

      {/* Floating 3D Interaction Hint */}
      <div className="viewport-drag-hint">
        <span className="drag-hint-pulse" />
        <span>🖱️ Drag to rotate 3D asset</span>
      </div>

      {/* Hero Glass Studio HUD */}
      <div className="login-hud-overlay">
        <div className="login-hud-card">
          <div className="hud-badge">
            <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
            <span>Pure Generative Text-to-3D AI</span>
          </div>

          <h1 className="hud-headline">
            Turn Words Into Game-Ready 3D Models
          </h1>

          <p className="hud-lead">
            Synthesize watertight manifold geometry, bake 1024px PBR textures, and optimize topology in seconds. Direct binary GLB export for Unreal Engine 5, Unity, and Blender.
          </p>

          {/* Interactive Text-to-3D Prompt Launcher */}
          <form onSubmit={handleLaunchWithPrompt} className="hud-prompt-box">
            <div className="hud-prompt-input-row">
              <input
                type="text"
                value={promptInput}
                onChange={(e) => setPromptInput(e.target.value)}
                placeholder="Describe any 3D asset (e.g. 'a round wooden table', 'a castle tower')..."
                className="hud-prompt-input"
              />
              <button type="submit" className="hud-generate-btn">
                <Sparkles className="w-4 h-4" />
                <span>Generate 3D</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Prompt Suggestions */}
            <div className="hud-suggestions-row">
              <span className="text-[11px] text-slate-400 font-medium">Try:</span>
              {SUGGESTED_PROMPTS.slice(0, 3).map((p, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectSuggestion(p)}
                  className="hud-suggestion-chip"
                >
                  {p.split(' ')[1] || p.split(' ')[0]}
                </button>
              ))}
            </div>
          </form>

          {/* Direct Launch & Auth Toggle Action Buttons */}
          <div className="hud-action-row">
            <button
              type="button"
              onClick={loginAsGuest}
              className="hud-primary-launch-btn"
            >
              <Zap className="w-4 h-4 text-amber-300" />
              <span>Instant Guest Access (Launch Studio)</span>
              <ArrowRight className="w-4 h-4 text-white" />
            </button>

            <button
              type="button"
              onClick={() => setShowAuthForm(!showAuthForm)}
              className="hud-secondary-auth-btn"
            >
              <User className="w-3.5 h-3.5 text-slate-300" />
              <span>{showAuthForm ? 'Hide Sign In' : 'Sign In / Register'}</span>
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showAuthForm ? 'rotate-180' : ''}`} />
            </button>
          </div>

          {/* Expandable Auth Credentials Form */}
          {showAuthForm && (
            <div className="hud-auth-drawer">
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

              {authError && (
                <div className="auth-alert-box">
                  <span>{authError}</span>
                </div>
              )}

              <form onSubmit={handleAuthSubmit} className="auth-input-form mt-3">
                <div className="auth-field-group">
                  <label className="auth-label">Username</label>
                  <div className="auth-input-wrapper">
                    <User className="w-3.5 h-3.5 text-slate-400" />
                    <input
                      type="text"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      placeholder="Username"
                      required
                      className="auth-text-input"
                    />
                  </div>
                </div>

                {isRegister && (
                  <div className="auth-field-group">
                    <label className="auth-label">Email</label>
                    <div className="auth-input-wrapper">
                      <Mail className="w-3.5 h-3.5 text-slate-400" />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="email@domain.com"
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
                  {isLoading ? 'Authenticating...' : (isRegister ? 'Create Account & Enter' : 'Sign In & Enter')}
                </button>
              </form>
            </div>
          )}

          {/* Micro Telemetry Pills */}
          <div className="hud-telemetry-pills">
            <div className="hud-pill">
              <Box className="w-3 h-3 text-cyan-400" />
              <span>Watertight Manifold</span>
            </div>
            <div className="hud-pill">
              <Layers className="w-3 h-3 text-purple-400" />
              <span>1024px PBR Maps</span>
            </div>
            <div className="hud-pill">
              <Zap className="w-3 h-3 text-amber-400" />
              <span>&lt; 1.0s Latency</span>
            </div>
            <div className="hud-pill">
              <ShieldCheck className="w-3 h-3 text-emerald-400" />
              <span>GLB & OBJ Export</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginDashboard;
