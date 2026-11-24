import {
  RotateCw,
  Sun,
  Image as ImageIcon,
  Layers,
  FileSpreadsheet,
  Sliders,
  Camera
} from 'lucide-react';
import type { RenderMode } from '../types';

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
}

export function CanvasControls({
  renderMode,
  setRenderMode,
  autoRotate,
  setAutoRotate,
  lightIntensity,
  setLightIntensity,
  hasTextures,
  onOpenTextures,
  explodeProgress,
  setExplodeProgress,
  onOpenBom,
  onToggleCustomizer,
  isCustomizerOpen,
  onCaptureSnapshot
}: CanvasControlsProps) {
  return (
    <div className="clean-studio-dock">
      {/* 1. Shading Modes Segment */}
      <div className="dock-segmented">
        <button
          type="button"
          onClick={() => setRenderMode('pbr')}
          className={`dock-seg-btn ${renderMode === 'pbr' ? 'active' : ''}`}
          title="Physically Based Textured Shading"
        >
          PBR
        </button>
        <button
          type="button"
          onClick={() => setRenderMode('shaded')}
          className={`dock-seg-btn ${renderMode === 'shaded' ? 'active' : ''}`}
          title="Matte Clay Surface"
        >
          Clay
        </button>
        <button
          type="button"
          onClick={() => setRenderMode('wireframe')}
          className={`dock-seg-btn ${renderMode === 'wireframe' ? 'active' : ''}`}
          title="Wireframe Mesh Topology"
        >
          Wire
        </button>
      </div>

      <div className="dock-divider" />

      {/* 2. Interactive Viewport Tools */}
      <div className="dock-actions">
        <button
          type="button"
          onClick={() => setAutoRotate((prev) => !prev)}
          className={`dock-icon-btn ${autoRotate ? 'active' : ''}`}
          title={autoRotate ? 'Pause Turntable' : 'Start Turntable Rotation'}
        >
          <RotateCw className="w-3.5 h-3.5" />
        </button>

        <button
          type="button"
          onClick={onToggleCustomizer}
          className={`dock-icon-btn ${isCustomizerOpen ? 'active' : ''}`}
          title="Viewport & Material Studio Controls"
        >
          <Sliders className="w-3.5 h-3.5" />
        </button>

        <button
          type="button"
          onClick={onCaptureSnapshot}
          className="dock-icon-btn"
          title="Capture High-Res Viewport PNG Snapshot"
        >
          <Camera className="w-3.5 h-3.5 text-sky-400" />
        </button>
      </div>

      <div className="dock-divider" />

      {/* 3. Kinematic Assembly Explode Slider */}
      <div className="dock-slider-item" title="Kinematic Exploded View Scrubber">
        <Layers className="w-3.5 h-3.5 text-cyan-400" />
        <input
          type="range"
          min={0}
          max={100}
          step={1}
          value={Math.round(explodeProgress * 100)}
          onChange={(e) => setExplodeProgress(Number(e.target.value) / 100)}
          className="clean-range-input dock-range"
        />
        <span className="dock-slider-label">
          {Math.round(explodeProgress * 100)}%
        </span>
      </div>

      <div className="dock-divider" />

      {/* 4. Telemetry Drawers & Maps */}
      <div className="dock-actions">
        <button
          type="button"
          onClick={onOpenBom}
          className="dock-text-btn text-emerald-400"
          title="Component Bill of Materials & Cost Telemetry"
        >
          <FileSpreadsheet className="w-3.5 h-3.5" />
          <span>BOM</span>
        </button>

        {hasTextures && (
          <button
            type="button"
            onClick={onOpenTextures}
            className="dock-text-btn text-purple-400"
            title="Inspect 1024px Albedo, Normal & Roughness Maps"
          >
            <ImageIcon className="w-3.5 h-3.5" />
            <span>Maps</span>
          </button>
        )}
      </div>

      <div className="dock-divider" />

      {/* 5. Lighting Intensity Slider */}
      <div className="dock-slider-item" title="Studio Lighting Intensity">
        <Sun className="w-3.5 h-3.5 text-amber-400" />
        <input
          type="range"
          min={0.3}
          max={2.5}
          step={0.1}
          value={lightIntensity}
          onChange={(e) => setLightIntensity(Number(e.target.value))}
          className="clean-range-input dock-range"
        />
      </div>
    </div>
  );
}
