import { RotateCw, Sun, Image as ImageIcon } from 'lucide-react';
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
}

export function CanvasControls({
  renderMode,
  setRenderMode,
  autoRotate,
  setAutoRotate,
  lightIntensity,
  setLightIntensity,
  hasTextures,
  onOpenTextures
}: CanvasControlsProps) {
  return (
    <div className="canvas-controls-overlay">
      {/* Mode switcher segmented button */}
      <div className="segmented-control">
        <button
          onClick={() => setRenderMode('pbr')}
          className={`segment-btn ${renderMode === 'pbr' ? 'active' : ''}`}
          title="PBR Textured Surface"
        >
          <span>PBR Textured</span>
        </button>
        <button
          onClick={() => setRenderMode('shaded')}
          className={`segment-btn ${renderMode === 'shaded' ? 'active' : ''}`}
          title="Clay Shaded Surface"
        >
          <span>Clay Shaded</span>
        </button>
        <button
          onClick={() => setRenderMode('wireframe')}
          className={`segment-btn ${renderMode === 'wireframe' ? 'active' : ''}`}
          title="Wireframe Topology"
        >
          <span>Wireframe</span>
        </button>
      </div>

      {/* Auto Rotate */}
      <button
        onClick={() => setAutoRotate((prev) => !prev)}
        className={`ctrl-btn ${autoRotate ? 'active' : ''}`}
        title="Toggle Turntable Rotation"
      >
        <RotateCw className="w-3.5 h-3.5" />
        <span>{autoRotate ? 'Rotate: On' : 'Rotate: Off'}</span>
      </button>

      {/* PBR Texture maps inspector button */}
      {hasTextures && (
        <button
          onClick={onOpenTextures}
          className="ctrl-btn btn-accent-glow"
          title="Inspect Albedo, Normal, and Roughness Maps"
        >
          <ImageIcon className="w-3.5 h-3.5 text-purple-400" />
          <span>Inspect PBR Maps</span>
        </button>
      )}

      {/* Light Intensity Slider */}
      <div className="ctrl-slider-group">
        <Sun className="w-3.5 h-3.5 text-amber-400" />
        <input
          type="range"
          min={0.3}
          max={2.5}
          step={0.1}
          value={lightIntensity}
          onChange={(e) => setLightIntensity(Number(e.target.value))}
          className="ctrl-range"
          title="Adjust Studio Lighting"
        />
      </div>
    </div>
  );
}
