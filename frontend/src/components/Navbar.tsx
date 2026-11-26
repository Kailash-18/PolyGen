import { useState } from 'react';
import {
  Sun,
  Moon,
  FolderOpen,
  ShieldCheck,
  ExternalLink,
  Code2,
  Wand2,
  Flame,
  LogOut
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
    <header className="clean-navbar vre-nav">
      {/* Brand Left with signature Hacks logo */}
      <div className="clean-nav-brand cursor-pointer" onClick={() => setActiveTab('studio')}>
        <svg className="vre-mark w-7 h-7" viewBox="0 0 32 32" aria-hidden="true">
          <path className="m3" d="M16 20.5 27 25.5 16 30.5 5 25.5Z" fill="#8b7bff" fillOpacity=".85" />
          <path className="m2" d="M16 11.5 27 16.5 16 21.5 5 16.5Z" fill="#4f8cff" fillOpacity=".9" />
          <path className="m1" d="M16 2.5 27 7.5 16 12.5 5 7.5Z" fill="#5ee6ff" />
        </svg>
        <div className="clean-brand-text">
          <span className="clean-nav-title">PolyGen 3D</span>
          <span className="clean-brand-sub">Text-to-3D AI Studio</span>
        </div>
        <div
          className="clean-engine-status"
          title={gpuInfo?.cuda_available ? `CUDA Active: ${gpuInfo.device_name}` : '3D Kinematics AI Engine Active'}
        >
          <span className="status-dot-pulse" />
          <span>{gpuInfo?.cuda_available ? 'CUDA' : '3D LIVE'}</span>
        </div>
      </div>

      {/* Laser-Optimized Text-to-3D Navigation Switcher */}
      <nav className="lab-switch" data-on={activeTab} aria-label="Text-to-3D Navigation">
        <button
          type="button"
          onClick={() => setActiveTab('studio')}
          className={`lab-switch-item ${activeTab === 'studio' ? 'active' : ''}`}
          title="Generative Text-to-3D Studio"
        >
          <Wand2 className="w-3.5 h-3.5" />
          <span>Text-to-3D</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('explore')}
          className={`lab-switch-item ${activeTab === 'explore' ? 'active' : ''}`}
          title="Explore Curated 3D Prompts & Inspirations"
        >
          <Flame className="w-3.5 h-3.5" />
          <span>Explore</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('library')}
          className={`lab-switch-item ${activeTab === 'library' ? 'active' : ''}`}
          title="My Generated 3D Asset Library"
        >
          <FolderOpen className="w-3.5 h-3.5" />
          <span>Library</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('audit')}
          className={`lab-switch-item ${activeTab === 'audit' ? 'active' : ''}`}
          title="AI Pipeline Latency & Telemetry"
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Telemetry</span>
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
          title="View PolyGen Source Repository on GitHub"
        >
          <Code2 className="w-3.5 h-3.5 text-slate-300" />
        </a>

        {/* Sign Out / Go to Login Page */}
        <button
          type="button"
          onClick={logout}
          className="clean-action-btn text-slate-300 hover:text-red-400"
          title="Sign Out / Switch to Login Page"
        >
          <LogOut className="w-3.5 h-3.5" />
        </button>

        {/* Profile Avatar / Menu */}
        <div className="profile-menu-container">
          <button
            type="button"
            onClick={() => setShowProfileMenu((prev) => !prev)}
            className="user-profile-badge"
            title="Studio Developer Profile"
          >
            <div className="profile-avatar">
              <span>{(user?.name || user?.displayName) ? (user.name || user.displayName)![0] : 'K'}</span>
            </div>
            <span className="profile-name hidden sm:inline">
              {user?.name || user?.displayName || 'Kailash'}
            </span>
          </button>

          {showProfileMenu && (
            <>
              <div
                className="fixed inset-0 z-40 bg-transparent"
                onClick={() => setShowProfileMenu(false)}
              />
              <div className="profile-dropdown-card">
                <div className="profile-dropdown-header">
                  <span className="font-semibold text-xs text-slate-100">
                    {user?.name || user?.displayName || 'Kailash'}
                  </span>
                  <span className="text-[10px] text-slate-400">{user?.email || 'admin@polygen.ai'}</span>
                  <span className="role-tag mt-1 text-[9px] bg-purple-500/20 text-purple-300 border border-purple-500/30 px-1.5 py-0.5 rounded w-max">
                    {user?.role || 'Lead 3D Architect'}
                  </span>
                </div>
                <div className="profile-dropdown-divider" />
                <a
                  href="https://github.com/Kailash-18/hacks"
                  target="_blank"
                  rel="noreferrer"
                  className="profile-dropdown-item"
                >
                  <ExternalLink className="w-3 h-3 text-indigo-400" />
                  <span>Teardown AI Repo</span>
                </a>
                <button
                  type="button"
                  onClick={logout}
                  className="profile-dropdown-item text-red-400 hover:text-red-300"
                >
                  <span>Sign Out</span>
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Navbar;
