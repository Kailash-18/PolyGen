import { Box } from 'lucide-react';

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
  { label: 'Broadsword', prompt: 'A rusted medieval broadsword with a glowing blue sapphire in the hilt' },
  { label: 'Knight Shield', prompt: 'A heavy knight tower shield with reinforced iron boss' },
  { label: 'Greek Vase', prompt: 'An ancient ceramic Greek vase with etched geometric patterns' },
  { label: 'Task Chair', prompt: 'A modern ergonomic office task chair with lumbar support' },
  { label: 'Cyber Crystal', prompt: 'A glowing hexagonal crystal cluster with obsidian base' }
];

const STYLES = ['Realistic PBR', 'Stylized Game', 'Sci-Fi Cyber', 'Antique'];
const POLY_PRESETS = [5000, 10000, 25000];

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
    <div className="clean-prompt-wrapper">
      {/* Quick Suggestion Ghost Chips */}
      <div className="clean-suggestion-row">
        {PRESETS.map((p) => (
          <button
            key={p.label}
            type="button"
            onClick={() => setPrompt(p.prompt)}
            disabled={isLoading}
            className={`clean-suggestion-chip ${prompt === p.prompt ? 'active' : ''}`}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Main Floating Capsule */}
      <div className="clean-prompt-capsule">
        <Box className="w-3.5 h-3.5 text-slate-400 shrink-0" />

        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !isLoading && onGenerate()}
          placeholder="Describe 3D geometry & texture (e.g. 'Rusted knight broadsword with sapphire')..."
          className="clean-prompt-input"
          disabled={isLoading}
        />

        {/* Style Selector Pill */}
        <div className="relative">
          <select
            value={stylePreset}
            onChange={(e) => setStylePreset(e.target.value)}
            disabled={isLoading}
            className="clean-select-pill"
            title="PBR Texture Style Preset"
          >
            {STYLES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        {/* Polycount Selector Pill */}
        <div className="relative">
          <select
            value={targetFaces}
            onChange={(e) => setTargetFaces(Number(e.target.value))}
            disabled={isLoading}
            className="clean-select-pill font-mono"
            title="Target Polycount (Faces)"
          >
            {POLY_PRESETS.map((n) => (
              <option key={n} value={n}>{(n / 1000)}k polys</option>
            ))}
          </select>
        </div>

        {/* Generate Action Button */}
        <button
          type="button"
          onClick={onGenerate}
          disabled={isLoading || !prompt.trim()}
          className="clean-generate-btn"
        >
          {isLoading ? (
            <div className="clean-btn-spinner" />
          ) : (
            <>
              <span>Generate</span>
              <kbd className="clean-kbd-badge">↵</kbd>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
