import { useState } from 'react';
import { X, Lock, Mail, User, Sparkles, ArrowRight } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export function AuthModal() {
  const { showAuthModal, setShowAuthModal, login } = useAuth();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('kailash@polygen.ai');
  const [password, setPassword] = useState('••••••••');
  const [name, setName] = useState('Kailash');

  if (!showAuthModal) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(email, password);
  };

  const handleDemoLogin = () => {
    login('kailash@polygen.ai', 'demo123');
  };

  return (
    <div className="modal-backdrop" onClick={() => setShowAuthModal(false)}>
      <div className="auth-modal-card" onClick={(e) => e.stopPropagation()}>
        <button
          className="modal-close-btn"
          onClick={() => setShowAuthModal(false)}
          aria-label="Close"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="auth-header">
          <div className="auth-logo-badge">
            <Sparkles className="w-5 h-5 text-purple-400" />
          </div>
          <h2 className="auth-title">
            {isSignUp ? 'Create PolyGen Account' : 'Welcome to PolyGen'}
          </h2>
          <p className="auth-sub">
            {isSignUp
              ? 'Start generating production-ready 3D game assets'
              : 'Sign in to access your 3D Asset Library & Studio'}
          </p>
        </div>

        {/* Demo Fast Login */}
        <button type="button" onClick={handleDemoLogin} className="demo-login-btn">
          <div className="flex items-center gap-2">
            <div className="demo-dot" />
            <span className="font-medium text-sm">Fast Demo Login (Kailash)</span>
          </div>
          <ArrowRight className="w-4 h-4 text-purple-400" />
        </button>

        <div className="auth-divider">
          <span>or sign in with email</span>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          {isSignUp && (
            <div className="auth-field">
              <label>Full Name</label>
              <div className="auth-input-wrapper">
                <User className="w-4 h-4 text-slate-400" />
                <input
                  type="text"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Kailash"
                  required
                />
              </div>
            </div>
          )}

          <div className="auth-field">
            <label>Email Address</label>
            <div className="auth-input-wrapper">
              <Mail className="w-4 h-4 text-slate-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="kailash@polygen.ai"
                required
              />
            </div>
          </div>

          <div className="auth-field">
            <label>Password</label>
            <div className="auth-input-wrapper">
              <Lock className="w-4 h-4 text-slate-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <button type="submit" className="auth-submit-btn">
            {isSignUp ? 'Create Account' : 'Sign In to Studio'}
          </button>
        </form>

        <div className="auth-footer-switch">
          <span>{isSignUp ? 'Already have an account?' : "Don't have an account?"}</span>
          <button
            type="button"
            onClick={() => setIsSignUp(!isSignUp)}
            className="auth-switch-link"
          >
            {isSignUp ? 'Sign In' : 'Sign Up'}
          </button>
        </div>
      </div>
    </div>
  );
}
