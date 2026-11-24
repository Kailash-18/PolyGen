import { Sliders, Eye, Sun, RotateCcw, X } from 'lucide-react';
import type { CameraPreset, ViewportSettings } from '../types';

interface ViewportCustomizerProps {
  isOpen: boolean;
  onClose: () => void;
  settings: ViewportSettings;
  setSettings: React.Dispatch<React.SetStateAction<ViewportSettings>>;
  cameraPreset: CameraPreset;
  setCameraPreset: (preset: CameraPreset) => void;
  onResetCamera: () => void;
}

const CLAY_COLORS = [
  { label: 'Slate', color: '#cbd5e1' },
  { label: 'Studio White', color: '#f8fafc' },
  { label: 'Terracotta', color: '#ea580c' },
  { label: 'Charcoal', color: '#334155' }
];

const WIREFRAME_COLORS = [
  { label: 'Cyan', color: '#38bdf8' },
  { label: 'Violet', color: '#a855f7' },
  { label: 'Amber', color: '#f59e0b' },
  { label: 'Chalk', color: '#ffffff' }
];

export function ViewportCustomizer({
  isOpen,
  onClose,
  settings,
  setSettings,
  cameraPreset,
  setCameraPreset,
  onResetCamera
}: ViewportCustomizerProps) {
  if (!isOpen) return null;

  return (
    <div className="customizer-panel">
      <div className="customizer-header">
        <div className="flex items-center gap-2">
          <Sliders className="w-4 h-4 text-purple-400" />
          <span className="customizer-title">Viewport & Material Studio</span>
        </div>
        <button
          onClick={onClose}
          type="button"
          className="customizer-close-btn"
          title="Close Customizer"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="customizer-content">
        {/* Camera Angles / Presets */}
        <div className="customizer-section">
          <label className="section-label">Camera Perspective</label>
          <div className="camera-preset-grid">
            {(
              [
                { id: 'default', label: 'Perspective' },
                { id: 'front', label: 'Front (1)' },
                { id: 'side', label: 'Side (3)' },
                { id: 'top', label: 'Top (7)' },
                { id: 'isometric', label: 'Iso' }
              ] as const
            ).map((p) => (
              <button
                key={p.id}
                type="button"
                onClick={() => setCameraPreset(p.id)}
                className={`preset-btn ${cameraPreset === p.id ? 'active' : ''}`}
              >
                {p.label}
              </button>
            ))}
            <button
              type="button"
              onClick={onResetCamera}
              className="preset-btn reset-btn"
              title="Reset View"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>
        </div>

        {/* Viewport Toggles (Grid & Shadows) */}
        <div className="customizer-section">
          <label className="section-label">Environment Display</label>
          <div className="toggle-row">
            <button
              type="button"
              onClick={() =>
                setSettings((prev) => ({ ...prev, showGrid: !prev.showGrid }))
              }
              className={`toggle-chip ${settings.showGrid ? 'active' : ''}`}
            >
              <Eye className="w-3.5 h-3.5" />
              <span>Ground Grid: {settings.showGrid ? 'ON' : 'OFF'}</span>
            </button>

            <button
              type="button"
              onClick={() =>
                setSettings((prev) => ({ ...prev, showShadows: !prev.showShadows }))
              }
              className={`toggle-chip ${settings.showShadows ? 'active' : ''}`}
            >
              <Sun className="w-3.5 h-3.5" />
              <span>Shadows: {settings.showShadows ? 'ON' : 'OFF'}</span>
            </button>
          </div>
        </div>

        {/* Clay Shaded Surface Tint */}
        <div className="customizer-section">
          <label className="section-label">Clay Shading Tone</label>
          <div className="color-swatch-row">
            {CLAY_COLORS.map((c) => (
              <button
                key={c.color}
                type="button"
                onClick={() =>
                  setSettings((prev) => ({ ...prev, clayColor: c.color }))
                }
                className={`color-swatch ${
                  settings.clayColor === c.color ? 'active' : ''
                }`}
                style={{ backgroundColor: c.color }}
                title={c.label}
              />
            ))}
            <span className="swatch-label">
              {CLAY_COLORS.find((c) => c.color === settings.clayColor)?.label || 'Custom'}
            </span>
          </div>
        </div>

        {/* Wireframe Color */}
        <div className="customizer-section">
          <label className="section-label">Wireframe Mesh Color</label>
          <div className="color-swatch-row">
            {WIREFRAME_COLORS.map((c) => (
              <button
                key={c.color}
                type="button"
                onClick={() =>
                  setSettings((prev) => ({ ...prev, wireframeColor: c.color }))
                }
                className={`color-swatch ${
                  settings.wireframeColor === c.color ? 'active' : ''
                }`}
                style={{ backgroundColor: c.color }}
                title={c.label}
              />
            ))}
            <span className="swatch-label">
              {WIREFRAME_COLORS.find((c) => c.color === settings.wireframeColor)?.label || 'Custom'}
            </span>
          </div>
        </div>

        {/* Live Material Tuning */}
        <div className="customizer-section">
          <div className="slider-header">
            <span className="section-label">Surface Roughness</span>
            <span className="slider-val">
              {Math.round(settings.roughnessMultiplier * 100)}%
            </span>
          </div>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={Math.round(settings.roughnessMultiplier * 100)}
            onChange={(e) =>
              setSettings((prev) => ({
                ...prev,
                roughnessMultiplier: Number(e.target.value) / 100
              }))
            }
            className="clean-range-input w-full"
          />
        </div>

        <div className="customizer-section">
          <div className="slider-header">
            <span className="section-label">Surface Metalness</span>
            <span className="slider-val">
              {Math.round(settings.metalnessMultiplier * 100)}%
            </span>
          </div>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={Math.round(settings.metalnessMultiplier * 100)}
            onChange={(e) =>
              setSettings((prev) => ({
                ...prev,
                metalnessMultiplier: Number(e.target.value) / 100
              }))
            }
            className="clean-range-input w-full"
          />
        </div>
      </div>
    </div>
  );
}
