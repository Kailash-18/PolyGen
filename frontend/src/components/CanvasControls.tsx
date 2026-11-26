import { useState } from 'react';
import {
  RotateCw,
  Sun,
  Layers,
  Sliders,
  Camera,
  ChevronDown
} from 'lucide-react';
import type { RenderMode, CameraPreset } from '../types';

interface CanvasControlsProps {
  renderMode: RenderMode;
  setRenderMode: (m: RenderMode) => void;
  autoRotate: boolean;
  setAutoRotate: (r: boolean | ((prev: boolean) => boolean)) => void;
  lightIntensity: number;
  setLightIntensity: (i: number) => void;
  hasTextures: boolean;
  onOpenTextures: () => void;
  explodeProgress: number;
  setExplodeProgress: (p: number) => void;
  onOpenBom: () => void;
  onToggleCustomizer: () => void;
  isCustomizerOpen: boolean;
  onCaptureSnapshot: () => void;
  cameraPreset?: CameraPreset;
  setCameraPreset?: (p: CameraPreset) => void;
}

export function CanvasControls({
  renderMode,
  setRenderMode,
  autoRotate,
  setAutoRotate,
  lightIntensity,
  setLightIntensity,
  explodeProgress,
  setExplodeProgress,
  onCaptureSnapshot,
  cameraPreset = 'default',
  setCameraPreset
}: CanvasControlsProps) {
  const [showSettings, setShowSettings] = useState(false);

  return (
    <div className="viewport-hud-pill-bar">
      {/* 1. Turntable 360 Rotation Toggle */}
      <button
        type="button"
        onClick={() => setAutoRotate((prev) => !prev)}
        className={`hud-pill-btn ${autoRotate ? 'active' : ''}`}
        title="Toggle 360° Turntable Rotation"
      >
        <RotateCw className={`w-3.5 h-3.5 ${autoRotate ? 'animate-spin-slow text-cyan-400' : 'text-slate-400'}`} />
        <span className="hidden sm:inline">Turntable</span>
        {autoRotate && <span className="hud-badge-dot" />}
      </button>

      <div className="hud-pill-divider" />

      {/* 2. Shading Mode Switcher (PBR / Clay / Wire) */}
      <div className="hud-shading-group">
        {(['pbr', 'shaded', 'wireframe'] as RenderMode[]).map((mode) => (
          <button
            key={mode}
            type="button"
            onClick={() => setRenderMode(mode)}
            className={`hud-sub-btn ${renderMode === mode ? 'active' : ''}`}
            title={`Switch to ${mode.toUpperCase()} Shading`}
          >
            {mode === 'pbr' ? 'PBR' : mode === 'shaded' ? 'Clay' : 'Wire'}
          </button>
        ))}
      </div>

      <div className="hud-pill-divider" />

      {/* 3. Exploded View Slider */}
      <div className="hud-explode-container" title="Pull Apart Kinematic 3D Assembly">
        <Layers className="w-3.5 h-3.5 text-purple-400 shrink-0" />
        <span className="text-[11px] font-semibold text-slate-300 hidden md:inline">Explode</span>
        <input
          type="range"
          min={0}
          max={100}
          step={1}
          value={Math.round(explodeProgress * 100)}
          onChange={(e) => setExplodeProgress(Number(e.target.value) / 100)}
          className="hud-slider-input"
        />
        <span className="text-[10px] font-mono text-purple-300 w-7 text-right">
          {Math.round(explodeProgress * 100)}%
        </span>
      </div>

      <div className="hud-pill-divider" />

      {/* 4. Instant HD Snapshot */}
      <button
        type="button"
        onClick={onCaptureSnapshot}
        className="hud-pill-btn"
        title="Capture 4K Transparent Viewport Render"
      >
        <Camera className="w-3.5 h-3.5 text-emerald-400" />
        <span className="hidden md:inline">Snapshot</span>
      </button>

      {/* 5. Studio Settings Popover (Camera Angles & Lighting) */}
      <div className="relative">
        <button
          type="button"
          onClick={() => setShowSettings((prev) => !prev)}
          className={`hud-pill-btn ${showSettings ? 'active' : ''}`}
          title="Camera Angles & Studio Lighting"
        >
          <Sliders className="w-3.5 h-3.5 text-indigo-400" />
          <span className="hidden lg:inline">Camera</span>
          <ChevronDown className="w-3 h-3 opacity-60" />
        </button>

        {showSettings && (
          <>
            <div className="fixed inset-0 z-40" onClick={() => setShowSettings(false)} />
            <div className="hud-settings-dropdown">
              <div className="text-[10px] font-bold text-slate-400 tracking-wider uppercase mb-2">
                Camera Angles
              </div>
              <div className="grid grid-cols-2 gap-1.5 mb-3">
                {(['isometric', 'front', 'side', 'top'] as CameraPreset[]).map((p) => (
                  <button
                    key={p}
                    type="button"
                    onClick={() => {
                      setCameraPreset && setCameraPreset(p);
                      setShowSettings(false);
                    }}
                    className={`hud-dropdown-btn ${cameraPreset === p ? 'active' : ''}`}
                  >
                    {p.toUpperCase()}
                  </button>
                ))}
              </div>

              <div className="hud-dropdown-divider" />

              <div className="flex items-center justify-between text-[11px] font-semibold text-slate-300 mb-1.5 mt-2">
                <div className="flex items-center gap-1.5">
                  <Sun className="w-3.5 h-3.5 text-amber-400" />
                  <span>Studio Lighting</span>
                </div>
                <span className="font-mono text-amber-300 text-[10px]">
                  {lightIntensity.toFixed(1)}x
                </span>
              </div>
              <input
                type="range"
                min={0.4}
                max={2.6}
                step={0.1}
                value={lightIntensity}
                onChange={(e) => setLightIntensity(Number(e.target.value))}
                className="hud-slider-input w-full"
              />
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default CanvasControls;
