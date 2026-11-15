import { Eye, RotateCw, Sun, Play, Pause, Layers, Zap, Activity, RotateCcw } from 'lucide-react';

interface CanvasControlsProps {
  wireframe: boolean;
  setWireframe: (w: boolean | ((prev: boolean) => boolean)) => void;
  autoRotate: boolean;
  setAutoRotate: (r: boolean | ((prev: boolean) => boolean)) => void;
  lightIntensity: number;
  setLightIntensity: (i: number) => void;
  // Exploded View & Kinematics Controls
  explodeProgress?: number;
  setExplodeProgress?: (p: number) => void;
  isPlayingLoop?: boolean;
  setIsPlayingLoop?: (p: boolean | ((prev: boolean) => boolean)) => void;
  isHoloMode?: boolean;
  setIsHoloMode?: (h: boolean | ((prev: boolean) => boolean)) => void;
  isXrayMode?: boolean;
  setIsXrayMode?: (x: boolean | ((prev: boolean) => boolean)) => void;
  onTriggerRipple?: () => void;
  onResetParts?: () => void;
}

export function CanvasControls({
  wireframe,
  setWireframe,
  autoRotate,
  setAutoRotate,
  lightIntensity,
  setLightIntensity,
  explodeProgress = 0,
  setExplodeProgress,
  isPlayingLoop = false,
  setIsPlayingLoop,
  isHoloMode = false,
  setIsHoloMode,
  isXrayMode = false,
  setIsXrayMode,
  onTriggerRipple,
  onResetParts
}: CanvasControlsProps) {
  return (
    <div className="canvas-controls-overlay">
      {/* Visual Render Controls */}
      <button
        onClick={() => setWireframe((prev) => !prev)}
        className={`ctrl-btn ${wireframe ? 'active' : ''}`}
        title="Toggle Wireframe"
      >
        <Eye className="w-4 h-4" />
        <span>{wireframe ? 'Wireframe' : 'Shaded'}</span>
      </button>

      <button
        onClick={() => setAutoRotate((prev) => !prev)}
        className={`ctrl-btn ${autoRotate ? 'active' : ''}`}
        title="Toggle Auto-Rotate"
      >
        <RotateCw className="w-4 h-4" />
        <span>{autoRotate ? 'Turntable: ON' : 'Turntable: OFF'}</span>
      </button>

      {/* Exploded View Slider */}
      {setExplodeProgress && (
        <div className="ctrl-slider-group" title="Exploded View Separation Factor">
          <Layers className="w-4 h-4 text-cyan-400" />
          <input
            type="range"
            min={0}
            max={100}
            step={1}
            value={Math.round(explodeProgress * 100)}
            onChange={(e) => setExplodeProgress(Number(e.target.value) / 100)}
            className="ctrl-range"
          />
          <span className="text-xs font-mono text-cyan-300 w-10">
            {Math.round(explodeProgress * 100)}%
          </span>
        </div>
      )}

      {/* Auto-Play Assembly Loop */}
      {setIsPlayingLoop && (
        <button
          onClick={() => setIsPlayingLoop((prev) => !prev)}
          className={`ctrl-btn ${isPlayingLoop ? 'active' : ''}`}
          title="Cinematic Auto-Play Assembly/Disassembly Loop"
        >
          {isPlayingLoop ? <Pause className="w-4 h-4 text-emerald-400" /> : <Play className="w-4 h-4 text-emerald-400" />}
          <span>{isPlayingLoop ? 'Loop: ON' : 'Auto-Loop'}</span>
        </button>
      )}

      {/* Teardown Wave Ripple Trigger */}
      {onTriggerRipple && (
        <button
          onClick={onTriggerRipple}
          className="ctrl-btn"
          title="Trigger Sequential Disassembly Wave"
        >
          <Layers className="w-4 h-4 text-purple-400" />
          <span>Ripple Wave</span>
        </button>
      )}

      {/* Hologram Blueprint Mode */}
      {setIsHoloMode && (
        <button
          onClick={() => setIsHoloMode((prev) => !prev)}
          className={`ctrl-btn ${isHoloMode ? 'active' : ''}`}
          title="Toggle Hologram Blueprint Shader"
        >
          <Zap className="w-4 h-4 text-sky-400" />
          <span>{isHoloMode ? 'Holo: ON' : 'Holo Blueprint'}</span>
        </button>
      )}

      {/* Laser X-Ray Scanner Mode */}
      {setIsXrayMode && (
        <button
          onClick={() => setIsXrayMode((prev) => !prev)}
          className={`ctrl-btn ${isXrayMode ? 'active' : ''}`}
          title="Toggle Laser X-Ray & Internal Wiring Scanner"
        >
          <Activity className="w-4 h-4 text-pink-400" />
          <span>{isXrayMode ? 'X-Ray: ON' : 'X-Ray Laser'}</span>
        </button>
      )}

      {/* Reset Parts Position */}
      {onResetParts && (
        <button
          onClick={onResetParts}
          className="ctrl-btn"
          title="Reset All Parts Home"
        >
          <RotateCcw className="w-4 h-4 text-gray-400" />
          <span>Reset</span>
        </button>
      )}

      {/* Studio Lighting Slider */}
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
