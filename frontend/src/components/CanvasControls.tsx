import { RotateCw, Sun, Image as ImageIcon, Layers, FileSpreadsheet } from 'lucide-react';
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
  onOpenBom
}: CanvasControlsProps) {
  return (
    <>
      {/* Top Left Floating Pill: Shading & Turntable */}
      <div className="canvas-float-left">
        <div className="clean-segmented">
          <button
            onClick={() => setRenderMode('pbr')}
            className={`clean-segment-btn ${renderMode === 'pbr' ? 'active' : ''}`}
            title="PBR Textured Surface"
          >
            Textured
          </button>
          <button
            onClick={() => setRenderMode('shaded')}
            className={`clean-segment-btn ${renderMode === 'shaded' ? 'active' : ''}`}
            title="Clay Shaded Surface"
          >
            Clay
          </button>
          <button
            onClick={() => setRenderMode('wireframe')}
            className={`clean-segment-btn ${renderMode === 'wireframe' ? 'active' : ''}`}
            title="Wireframe Topology"
          >
            Wireframe
          </button>
        </div>

        <button
          onClick={() => setAutoRotate((prev) => !prev)}
          className={`clean-icon-pill ${autoRotate ? 'active' : ''}`}
          title={autoRotate ? 'Pause Turntable Rotation' : 'Start Turntable Rotation'}
        >
          <RotateCw className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Top Right Floating Pill: Tools & Inspection */}
      <div className="canvas-float-right">
        {/* Exploded View Slider */}
        <div className="clean-slider-item" title="Kinematic Exploded View">
          <Layers className="w-3.5 h-3.5 text-cyan-400" />
          <input
            type="range"
            min={0}
            max={100}
            step={1}
            value={Math.round(explodeProgress * 100)}
            onChange={(e) => setExplodeProgress(Number(e.target.value) / 100)}
            className="clean-range-input"
          />
          <span className="clean-slider-text">
            {Math.round(explodeProgress * 100)}%
          </span>
        </div>

        {/* BOM Button */}
        <button
          onClick={onOpenBom}
          className="clean-tool-btn text-emerald-400"
          title="Bill of Materials & Cost"
        >
          <FileSpreadsheet className="w-3.5 h-3.5" />
          <span>BOM</span>
        </button>

        {/* PBR Maps Button */}
        {hasTextures && (
          <button
            onClick={onOpenTextures}
            className="clean-tool-btn text-purple-400"
            title="PBR Maps Inspector"
          >
            <ImageIcon className="w-3.5 h-3.5" />
            <span>Maps</span>
          </button>
        )}

        {/* Light Slider */}
        <div className="clean-slider-item" title="Studio Lighting Intensity">
          <Sun className="w-3.5 h-3.5 text-amber-400" />
          <input
            type="range"
            min={0.3}
            max={2.5}
            step={0.1}
            value={lightIntensity}
            onChange={(e) => setLightIntensity(Number(e.target.value))}
            className="clean-range-input"
          />
        </div>
      </div>
    </>
  );
}
