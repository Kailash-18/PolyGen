import { Sparkles, Layers, Palette } from 'lucide-react';

interface PromptBarProps {
  prompt: string;
  setPrompt: (p: string) => void;
  targetFaces: number;
  setTargetFaces: (f: number) => void;
  stylePreset: string;
  setStylePreset: (s: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

const PRESETS = [
  "A rusted medieval broadsword with a glowing blue sapphire in the hilt",
  "A heavy knight tower shield with reinforced iron boss",
  "An ancient ceramic Greek vase with etched geometric patterns",
  "A gothic carved wooden chair",
  "A glowing hexagonal crystal cluster with obsidian base"
];

const STYLES = ['Realistic PBR', 'Stylized Game', 'Sci-Fi Cyber', 'Antique'];

export function PromptBar({
  prompt,
  setPrompt,
  targetFaces,
  setTargetFaces,
  stylePreset,
  setStylePreset,
  onGenerate,
  isLoading
}: PromptBarProps) {
  return (
    <div className="prompt-container">
      <div className="prompt-card">
        <div className="prompt-input-row">
          <div className="input-wrapper">
            <Sparkles className="input-icon" />
            <input
              type="text"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !isLoading && onGenerate()}
              placeholder="Describe a 3D asset (e.g. 'A rusted medieval broadsword with sapphire in hilt')..."
              className="prompt-input"
              disabled={isLoading}
            />
          </div>

          <button
            onClick={onGenerate}
            disabled={isLoading || !prompt.trim()}
            className="generate-btn"
          >
            {isLoading ? (
              <>
                <div className="btn-spinner" />
                <span>Generating Asset...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Generate 3D Asset</span>
              </>
            )}
          </button>
        </div>

        {/* Options Row */}
        <div className="options-row">
          <div className="slider-group">
            <Layers className="w-3.5 h-3.5 text-slate-400" />
            <span className="slider-label">Decimation:</span>
            <input
              type="range"
              min={2000}
              max={50000}
              step={1000}
              value={targetFaces}
              onChange={(e) => setTargetFaces(Number(e.target.value))}
              disabled={isLoading}
              className="range-slider"
            />
            <span className="slider-val">{targetFaces.toLocaleString()} polys</span>
          </div>

          {/* Style Presets */}
          <div className="style-group">
            <Palette className="w-3.5 h-3.5 text-slate-400" />
            <span className="slider-label">Texture Style:</span>
            <div className="style-chips">
              {STYLES.map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setStylePreset(s)}
                  className={`style-chip-btn ${stylePreset === s ? 'active' : ''}`}
                  disabled={isLoading}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          {/* Quick presets */}
          <div className="preset-chips">
            <span className="presets-label">Quick Prompts:</span>
            {PRESETS.map((p, idx) => {
              const label = p.includes('broadsword')
                ? 'Sword'
                : p.includes('shield')
                ? 'Shield'
                : p.includes('vase')
                ? 'Vase'
                : p.includes('chair')
                ? 'Chair'
                : 'Crystal';
              return (
                <button
                  key={idx}
                  type="button"
                  onClick={() => setPrompt(p)}
                  disabled={isLoading}
                  className="chip-btn"
                >
                  {label}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
