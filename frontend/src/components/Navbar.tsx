import { useState } from 'react';
import {
  Box,
  Sun,
  Moon,
  FolderOpen,
  ShieldCheck,
  LogOut,
  ExternalLink,
  Code2,
  ChevronDown,
  Layers
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
    <header className="clean-navbar">
      {/* Brand Left */}
      <div className="clean-nav-brand" onClick={() => setActiveTab('studio')}>
        <div className="clean-nav-logo">
          <Box className="w-3.5 h-3.5 text-purple-400" />
        </div>
        <span className="clean-nav-title">PolyGen</span>
        <div
          className="clean-engine-status"
          title={gpuInfo?.cuda_available ? `CUDA Active: ${gpuInfo.device_name}` : 'Hybrid 3D Pipeline Ready'}
        >
          <span className="status-dot-pulse" />
          <span>{gpuInfo?.cuda_available ? 'CUDA' : 'Ready'}</span>
        </div>
      </div>

      {/* Navigation Tabs Center */}
      <nav className="clean-nav-tabs">
        <button
          type="button"
          onClick={() => setActiveTab('studio')}
          className={`clean-nav-tab ${activeTab === 'studio' ? 'active' : ''}`}
        >
          <Box className="w-3.5 h-3.5" />
          <span>Studio</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('library')}
          className={`clean-nav-tab ${activeTab === 'library' ? 'active' : ''}`}
        >
          <FolderOpen className="w-3.5 h-3.5" />
          <span>Library</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('audit')}
          className={`clean-nav-tab ${activeTab === 'audit' ? 'active' : ''}`}
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Audit</span>
        </button>
      </nav>

      {/* Utilities Right */}
      <div className="clean-nav-actions">
        {/* Theme Toggle */}
        <button
          type="button"
          onClick={toggleTheme}
          className="clean-action-btn"
          title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
        >
          {theme === 'dark' ? (
            <Sun className="w-3.5 h-3.5 text-amber-400" />
          ) : (
            <Moon className="w-3.5 h-3.5 text-purple-500" />
          )}
        </button>

        {/* GitHub Link */}
        <a
          href="https://github.com/Kailash-18/PolyGen"
          target="_blank"
          rel="noreferrer"
          className="clean-action-btn"
          title="GitHub Repository"
        >
          <Code2 className="w-3.5 h-3.5 text-slate-400" />
        </a>

        {/* User Profile Pill */}
        <div className="relative">
          <button
            type="button"
            onClick={() => setShowProfileMenu((prev) => !prev)}
            className="clean-user-pill"
          >
            <span className="clean-user-avatar">
              {user?.name ? user.name[0].toUpperCase() : 'K'}
            </span>
            <span className="clean-user-name">{user?.name || 'Sri Kailash'}</span>
            <ChevronDown className="w-3 h-3 text-slate-400" />
          </button>

          {showProfileMenu && (
            <div className="clean-dropdown-menu">
              <div className="dropdown-user-info">
                <span className="font-semibold text-xs text-slate-200">
                  {user?.name || 'Sri Kailash'}
                </span>
                <span className="text-[11px] text-slate-400">
                  {user?.role || 'Studio Lead'} · {user?.email || 'sri.anjaneya.kailash@gmail.com'}
                </span>
              </div>
              <div className="dropdown-divider" />
              <a
                href="/viewer/"
                target="_blank"
                rel="noreferrer"
                className="dropdown-item-link"
              >
                <Layers className="w-3.5 h-3.5 text-slate-400" />
                <span>Physical Assembly Lab</span>
                <ExternalLink className="w-3 h-3 opacity-40 ml-auto" />
              </a>
              <a
                href="/viewer/build.html"
                target="_blank"
                rel="noreferrer"
                className="dropdown-item-link"
              >
                <Box className="w-3.5 h-3.5 text-slate-400" />
                <span>Digital Engineering Lab</span>
                <ExternalLink className="w-3 h-3 opacity-40 ml-auto" />
              </a>
              <div className="dropdown-divider" />
              <button
                type="button"
                onClick={() => {
                  setShowProfileMenu(false);
                  logout();
                }}
                className="dropdown-logout-btn"
              >
                <LogOut className="w-3.5 h-3.5 text-rose-400" />
                <span>Sign Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
