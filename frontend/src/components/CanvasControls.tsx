import { Eye, RotateCw, Sun } from 'lucide-react';

interface CanvasControlsProps {
  wireframe: boolean;
  setWireframe: (w: boolean | ((prev: boolean) => boolean)) => void;
  autoRotate: boolean;
  setAutoRotate: (r: boolean | ((prev: boolean) => boolean)) => void;
  lightIntensity: number;
  setLightIntensity: (i: number) => void;
}

export function CanvasControls({
  wireframe,
  setWireframe,
  autoRotate,
  setAutoRotate,
  lightIntensity,
  setLightIntensity
}: CanvasControlsProps) {
  return (
    <div className="canvas-controls-overlay">
      <button
        onClick={() => setWireframe((prev) => !prev)}
        className={`ctrl-btn ${wireframe ? 'active' : ''}`}
        title="Toggle Wireframe"
      >
        <Eye className="w-4 h-4" />
        <span>{wireframe ? 'Mesh: Wireframe' : 'Mesh: Shaded'}</span>
      </button>

      <button
        onClick={() => setAutoRotate((prev) => !prev)}
        className={`ctrl-btn ${autoRotate ? 'active' : ''}`}
        title="Toggle Auto-Rotate"
      >
        <RotateCw className="w-4 h-4" />
        <span>{autoRotate ? 'Turntable: On' : 'Turntable: Off'}</span>
      </button>

      <div className="ctrl-slider-group">
        <Sun className="w-4 h-4 text-amber-400" />
        <input
          type="range"
          min={0.2}
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
