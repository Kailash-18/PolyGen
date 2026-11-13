import { Sparkles, Layers } from 'lucide-react';

interface PromptBarProps {
  prompt: string;
  setPrompt: (p: string) => void;
  targetFaces: number;
  setTargetFaces: (f: number) => void;
  onGenerate: () => void;
  isLoading: boolean;
}

const PRESETS = [
  "A rusted medieval broadsword with a glowing blue sapphire in the hilt",
  "An ancient ceramic Greek vase with etched geometric patterns",
  "A glowing hexagonal crystal cluster with obsidian base",
  "A heavy knight tower shield with reinforced iron boss",
  "A gothic carved wooden chair"
];

export function PromptBar({
  prompt,
  setPrompt,
  targetFaces,
  setTargetFaces,
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
              placeholder="Describe a 3D asset (e.g. 'A rusted medieval broadsword...')"
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
                <span>Generating 3D Mesh...</span>
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
            <span className="slider-label">Target Decimation:</span>
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

          {/* Quick presets */}
          <div className="preset-chips">
            <span className="presets-label">Quick Prompts:</span>
            {PRESETS.map((p, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setPrompt(p)}
                disabled={isLoading}
                className="chip-btn"
              >
                {p.split(' ')[1] || 'Item'}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
