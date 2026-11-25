import React, { useState } from 'react';
import {
  ArrowUp,
  Maximize2,
  Minimize2,
  Layers,
  Wand2
} from 'lucide-react';

interface PromptBarProps {
  prompt: string;
  setPrompt: (p: string) => void;
  targetFaces: number;
  setTargetFaces: (f: number) => void;
  stylePreset: string;
  setStylePreset: (s: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
  onOpenSamples: () => void;
}

const STYLES = ['Realistic PBR', 'Stylized Game', 'Sci-Fi Cyber', 'Antique', 'Low Poly CAD'];
const POLY_PRESETS = [5000, 10000, 25000];

export function PromptBar({
  prompt,
  setPrompt,
  targetFaces,
  setTargetFaces,
  stylePreset,
  setStylePreset,
  onGenerate,
  isLoading,
  onOpenSamples
}: PromptBarProps) {
  // Start in big Hero prompt mode when opening, transition to iOS style once typing or generating
  const [isHeroMode, setIsHeroMode] = useState<boolean>(true);
  const [hasInteracted, setHasInteracted] = useState<boolean>(false);

  // Transition to iOS dock mode when user types or generates
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setPrompt(e.target.value);
    if (!hasInteracted && e.target.value.trim().length > 0) {
      setHasInteracted(true);
      // smoothly transition to iOS dock mode once user begins entering their custom vision
      setIsHeroMode(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && prompt.trim()) {
        setIsHeroMode(false);
        onGenerate();
      }
    }
  };

  // --------------------------------------------------------------------------
  // MODE 1: BIG HERO PROMPT BOX ("What do you want to build?")
  // --------------------------------------------------------------------------
  if (isHeroMode) {
    return (
      <div className="hero-prompt-overlay">
        <div className="hero-prompt-card">
          <div className="hero-prompt-header">
            <div className="flex items-center gap-2">
              <div className="hero-prompt-icon-badge">
                <Wand2 className="w-4 h-4 text-purple-400" />
              </div>
              <div>
                <h2 className="hero-prompt-title">What do you want to build?</h2>
                <p className="hero-prompt-sub">
                  Describe any 3D asset and PolyGen will synthesize manifold geometry with full PBR textures
                </p>
              </div>
            </div>

            <button
              type="button"
              onClick={() => setIsHeroMode(false)}
              className="hero-dock-toggle-btn"
              title="Dock to iOS bar at bottom"
            >
              <Minimize2 className="w-3.5 h-3.5" />
              <span>Dock to bottom</span>
            </button>
          </div>

          {/* Big Input Area */}
          <div className="hero-prompt-input-wrapper">
            <textarea
              value={prompt}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              placeholder="Describe what you want to build (e.g. 'A rusted medieval broadsword with a glowing blue sapphire in the hilt')..."
              rows={3}
              className="hero-prompt-textarea"
              disabled={isLoading}
              autoFocus
            />
          </div>

          {/* Controls & Action Row */}
          <div className="hero-prompt-footer">
            <div className="flex items-center gap-2 flex-wrap">
              {/* Dedicated Separate Samples Button */}
              <button
                type="button"
                onClick={onOpenSamples}
                className="hero-samples-pill-btn"
                title="Browse Pre-Engineered 3D Samples"
              >
                <Layers className="w-3.5 h-3.5 text-purple-400" />
                <span>Samples Catalog</span>
              </button>

              {/* Style selector */}
              <select
                value={stylePreset}
                onChange={(e) => setStylePreset(e.target.value)}
                disabled={isLoading}
                className="clean-select-pill"
                title="Texture Style Preset"
              >
                {STYLES.map((s) => (
                  <option key={s} value={s}>{s}</option>
                ))}
              </select>

              {/* Polycount target */}
              <select
                value={targetFaces}
                onChange={(e) => setTargetFaces(Number(e.target.value))}
                disabled={isLoading}
                className="clean-select-pill font-mono"
                title="Target Polygon Density"
              >
                {POLY_PRESETS.map((n) => (
                  <option key={n} value={n}>{(n / 1000)}k polygons</option>
                ))}
              </select>
            </div>

            {/* Synthesize Button */}
            <button
              type="button"
              onClick={() => {
                setIsHeroMode(false);
                onGenerate();
              }}
              disabled={isLoading || !prompt.trim()}
              className="hero-generate-action-btn"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="clean-spinner" />
                  <span>Synthesizing...</span>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <span>Synthesize 3D</span>
                  <ArrowUp className="w-3.5 h-3.5" />
                </div>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // --------------------------------------------------------------------------
  // MODE 2: SLEEK iOS-STYLE BOTTOM DYNAMIC CAPSULE
  // --------------------------------------------------------------------------
  return (
    <div className="ios-prompt-dock-wrapper">
      <div className="ios-prompt-capsule">
        {/* Dedicated Separate Samples Button */}
        <button
          type="button"
          onClick={onOpenSamples}
          className="ios-samples-btn"
          title="Browse 3D Samples Catalog"
        >
          <Layers className="w-3.5 h-3.5 text-purple-400" />
          <span className="hidden sm:inline">Samples</span>
        </button>

        <div className="ios-dock-divider" />

        {/* Input */}
        <input
          type="text"
          value={prompt}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="What do you want to build? (Type to describe 3D asset)..."
          className="ios-prompt-input"
          disabled={isLoading}
        />

        {/* Style selector */}
        <select
          value={stylePreset}
          onChange={(e) => setStylePreset(e.target.value)}
          disabled={isLoading}
          className="ios-select-chip"
          title="Style"
        >
          {STYLES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>

        {/* Polycount */}
        <select
          value={targetFaces}
          onChange={(e) => setTargetFaces(Number(e.target.value))}
          disabled={isLoading}
          className="ios-select-chip font-mono"
          title="Polycount Target"
        >
          {POLY_PRESETS.map((n) => (
            <option key={n} value={n}>{(n / 1000)}k</option>
          ))}
        </select>

        {/* Expand back to big Hero box */}
        <button
          type="button"
          onClick={() => setIsHeroMode(true)}
          className="ios-expand-icon-btn"
          title="Expand to big prompt card"
        >
          <Maximize2 className="w-3.5 h-3.5" />
        </button>

        {/* Circular iOS Send Button */}
        <button
          type="button"
          onClick={onGenerate}
          disabled={isLoading || !prompt.trim()}
          className={`ios-send-button ${prompt.trim() ? 'active' : ''}`}
          title="Generate 3D Asset (Enter)"
        >
          {isLoading ? (
            <div className="ios-send-spinner" />
          ) : (
            <ArrowUp className="w-4 h-4 text-white stroke-[2.5]" />
          )}
        </button>
      </div>
    </div>
  );
}

export default PromptBar;