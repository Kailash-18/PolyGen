import { useState } from 'react';
import {
  Box,
  Cpu,
  Code2,
  Sun,
  Moon,
  FolderOpen,
  Sparkles,
  ClipboardCheck,
  LogOut,
  ChevronDown,
  ExternalLink
} from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { useAuth } from '../context/AuthContext';
import type { ActiveTab } from '../types';

interface NavbarProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  gpuInfo?: {
    cuda_available: boolean;
    device_name: string;
  };
}

export function Navbar({ activeTab, setActiveTab, gpuInfo }: NavbarProps) {
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  return (
    <header className="navbar">
      <div className="nav-left">
        <div className="nav-brand" onClick={() => setActiveTab('studio')} style={{ cursor: 'pointer' }}>
          <div className="nav-logo">
            <Box className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <div className="brand-title">
              <span>Poly</span><span className="brand-accent">Gen</span>
            </div>
            <p className="brand-sub">Generative Text-to-3D Asset Pipeline</p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="nav-tabs">
          <button
            onClick={() => setActiveTab('studio')}
            className={`nav-tab-btn ${activeTab === 'studio' ? 'active' : ''}`}
          >
            <Sparkles className="w-4 h-4" />
            <span>3D Studio</span>
          </button>

          <button
            onClick={() => setActiveTab('library')}
            className={`nav-tab-btn ${activeTab === 'library' ? 'active' : ''}`}
          >
            <FolderOpen className="w-4 h-4" />
            <span>Asset Library</span>
          </button>

          <button
            onClick={() => setActiveTab('audit')}
            className={`nav-tab-btn ${activeTab === 'audit' ? 'active' : ''}`}
          >
            <ClipboardCheck className="w-4 h-4" />
            <span>Mid-Project Audit</span>
          </button>
        </nav>
      </div>

      <div className="nav-actions">
        {/* Collaborator Lab Links */}
        <a
          href="/viewer/"
          target="_blank"
          rel="noreferrer"
          className="lab-link-pill"
          title="Open Physical 3D Assembly Lab"
        >
          <span>Physical Lab</span>
          <ExternalLink className="w-3 h-3 text-cyan-400" />
        </a>

        <a
          href="/viewer/build.html"
          target="_blank"
          rel="noreferrer"
          className="lab-link-pill"
          title="Open Digital Engineering Lab"
        >
          <span>Digital Lab</span>
          <ExternalLink className="w-3 h-3 text-purple-400" />
        </a>

        {/* GPU Status Pill */}
        <div className="gpu-badge" title="Hardware Acceleration Status">
          <Cpu className="w-3.5 h-3.5 text-emerald-400" />
          <span>{gpuInfo?.cuda_available ? gpuInfo.device_name : 'Local Engine Ready'}</span>
        </div>

        {/* Dark / Light Mode Switcher */}
        <button
          onClick={toggleTheme}
          className="theme-toggle-btn"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-purple-600" />
          )}
        </button>

        {/* GitHub Link */}
        <a
          href="https://github.com/Kailash-18/PolyGen"
          target="_blank"
          rel="noreferrer"
          className="github-btn"
          title="View GitHub Repository"
        >
          <Code2 className="w-4 h-4" />
          <span>GitHub</span>
        </a>

        {/* User Auth Profile (Only rendered when logged in) */}
        {user && (
          <div className="user-profile-wrapper">
            <button
              onClick={() => setShowProfileMenu(!showProfileMenu)}
              className="user-pill-btn"
            >
              <img
                src={user.avatar}
                alt={user.name}
                className="user-avatar-img"
              />
              <div className="user-text-info">
                <span className="user-name">{user.name}</span>
                <span className="user-plan">{user.plan}</span>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {showProfileMenu && (
              <div className="profile-dropdown-menu">
                <div className="dropdown-user-header">
                  <p className="dropdown-name">{user.name}</p>
                  <p className="dropdown-email">{user.email}</p>
                  <span className="dropdown-role">{user.role}</span>
                </div>
                <div className="dropdown-divider" />
                <button
                  onClick={() => {
                    setActiveTab('library');
                    setShowProfileMenu(false);
                  }}
                  className="dropdown-item"
                >
                  <FolderOpen className="w-4 h-4" />
                  <span>My 3D Projects</span>
                </button>
                <button
                  onClick={() => {
                    toggleTheme();
                    setShowProfileMenu(false);
                  }}
                  className="dropdown-item"
                >
                  {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                  <span>{theme === 'dark' ? 'Light Mode' : 'Dark Mode'}</span>
                </button>
                <div className="dropdown-divider" />
                <button
                  onClick={() => {
                    logout();
                    setShowProfileMenu(false);
                  }}
                  className="dropdown-item text-rose-400"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
