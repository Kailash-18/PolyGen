import React, { useState } from 'react';
import {
  Sparkles,
  Layers,
  ArrowUp,
  Cpu,
  Dices,
  SlidersHorizontal,
  ChevronDown,
  ChevronUp,
  ShieldAlert
} from 'lucide-react';

interface PromptBarProps {
  prompt: string;
  setPrompt: (p: string) => void;
  targetFaces: number;
  setTargetFaces: (f: number) => void;
  stylePreset: string;
  setStylePreset: (s: string) => void;
  onGenerate: () => void;
  isLoading: boolean;
  onOpenSamples: () => void;
  negativePrompt?: string;
  setNegativePrompt?: (np: string) => void;
}

const STYLES = ['Realistic PBR', 'Sci-Fi Cyber', 'Stylized Fantasy', 'Antique Bronze', 'Low Poly CAD'];
const POLY_PRESETS = [5000, 10000, 25000];

const SURPRISE_PROMPTS = [
  'A sleek aerodynamic futuristic sports car with glowing neon cyan rims, carbon fiber diffusers, and aggressive front splitters',
  'A masterwork folded Damascus steel broadsword with gold inlay runic engravings and a sapphire pommel',
  'A deep-space exploratory starfighter with swept delta wings, dual plasma ion thrusters, and matte stealth cockpit canopy',
  'A heavy bipedal combat mech with shoulder missile pods, reinforced knee actuators, and dual rotary plasma miniguns',
  'A cluster of glowing prismatic quartz mana crystals on dark basalt bedrock with ethereal violet bioluminescence',
  'A bearded Viking battleaxe with carved Nordic elder Futhark runes, bronze collar, and cross-stitched leather haft',
  'An ornate pirate treasure chest with wrought-iron banding, carved oak staves, and brass lion-head lock plate',
  'A teardrop alchemical potion flask with glowing ruby healing elixir and filigree brass cage',
  'An ancient Greek terracotta amphora vase with fluted neck and mythological warrior meander frieze',
  'A tactical reconnaissance drone with folding carbon-fiber arms and spherical optical sensor dome',
  'A futuristic pulse plasma rifle with glowing cyan heat sinks, top holo-sight, and textured grip',
  'A dwarven war hammer with dual-sided steel striking faces and rune-chiseled granite core',
  'A cybernetic samurai helmet with glowing crimson visor and gold-plated crest ornament',
  'A floating miniature bonsai tree on a chunk of mossy levitating bedrock with exposed roots',
  'A glowing quantum power core with magnetic levitation stabilizer rings and copper induction coils'
];

const SUGGESTIONS = [
  { label: '🏎️ Sports Car', prompt: 'A sleek aerodynamic futuristic sports car with glowing neon rims' },
  { label: '⚔️ Katana', prompt: 'A Japanese katana with folded Damascus steel blade and golden dragon tsuba' },
  { label: '🚀 Starfighter', prompt: 'A sci-fi starfighter spaceship with swept delta wings and dual plasma thrusters' },
  { label: '🤖 Combat Mech', prompt: 'A heavy bipedal combat mech with shoulder missile pods and rotary miniguns' },
  { label: '💎 Mana Crystal', prompt: 'A cluster of glowing prismatic quartz mana crystals on dark bedrock' },
  { label: '🪓 Viking Axe', prompt: 'A bearded Viking battleaxe with carved Nordic runes and leather wrapped haft' },
  { label: '📦 Treasure Chest', prompt: 'An ornate pirate treasure chest with gold bindings and brass lock plate' },
  { label: '🧪 Health Potion', prompt: 'A magical glass flask with glowing crimson healing elixir and wooden cork' },
  { label: '🏺 Greek Amphora', prompt: 'An ancient Greek terracotta amphora vase with fluted belly and dual handles' },
];

export function PromptBar({
  prompt,
  setPrompt,
  targetFaces,
  setTargetFaces,
  stylePreset,
  setStylePreset,
  onGenerate,
  isLoading,
  onOpenSamples,
  negativePrompt = 'blurry, distorted, holes, non-manifold, low quality',
  setNegativePrompt
}: PromptBarProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [isEnhancing, setIsEnhancing] = useState(false);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (!isLoading && prompt.trim()) {
        onGenerate();
      }
    }
  };

  const handleSurpriseMe = () => {
    const randomPrompt = SURPRISE_PROMPTS[Math.floor(Math.random() * SURPRISE_PROMPTS.length)];
    setPrompt(randomPrompt);
  };

  const handleEnhancePrompt = () => {
    if (!prompt.trim()) {
      handleSurpriseMe();
      return;
    }
    setIsEnhancing(true);

    // AI Prompt Expansion Logic: enriches keywords with high-end generative 3D modifiers
    const p = prompt.trim();
    let enhanced = p;

    if (!/pbr|photorealistic|detailed|4k|8k|textured|finish/i.test(p)) {
      if (stylePreset === 'Realistic PBR') {
        enhanced += ', masterwork photorealistic 8k PBR materials, micro-surface imperfections, bevels';
      } else if (stylePreset === 'Sci-Fi Cyber') {
        enhanced += ', high-tech cybernetic panels, emissive neon accent glow, matte carbon fiber texture';
      } else if (stylePreset === 'Stylized Fantasy') {
        enhanced += ', vibrant hand-painted RPG fantasy style, clean game-ready topology, sharp silhouette';
      } else if (stylePreset === 'Antique Bronze') {
        enhanced += ', weathered bronze patina, oxidized verdigris accents, antique museum finish';
      } else {
        enhanced += ', clean manifold CAD geometry, optimal bevel highlights, crisp geometric definition';
      }
    }

    setTimeout(() => {
      setPrompt(enhanced);
      setIsEnhancing(false);
    }, 280);
  };

  return (
    <div className="studio-prompt-container">
      {/* Quick Suggestion Chips Row with AI Enhance & Surprise Me */}
      <div className="prompt-suggestions-row">
        <button
          type="button"
          onClick={handleSurpriseMe}
          className="suggestion-chip special-btn"
          title="Pick a random high-detail prompt"
          disabled={isLoading}
        >
          <Dices className="w-3.5 h-3.5 text-amber-400" />
          <span>Surprise Me</span>
        </button>

        <button
          type="button"
          onClick={handleEnhancePrompt}
          className="suggestion-chip special-btn"
          title="AI Prompt Enhancer: Enriches prompt with materials, lighting & micro-details"
          disabled={isLoading || isEnhancing}
        >
          <Sparkles className="w-3.5 h-3.5 text-purple-400" />
          <span>{isEnhancing ? 'Enhancing...' : 'AI Enhance'}</span>
        </button>

        <div className="suggestion-divider" />

        {SUGGESTIONS.map((item) => (
          <button
            key={item.label}
            type="button"
            className="suggestion-chip"
            onClick={() => setPrompt(item.prompt)}
            disabled={isLoading}
            title={item.prompt}
          >
            {item.label}
          </button>
        ))}
      </div>

      {/* Advanced Negative Prompt Drawer */}
      {showAdvanced && (
        <div className="prompt-advanced-drawer">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
            <span>Negative Prompt:</span>
          </div>
          <input
            type="text"
            value={negativePrompt}
            onChange={(e) => setNegativePrompt && setNegativePrompt(e.target.value)}
            placeholder="Features to avoid (e.g. 'blurry, holes, distorted, bad topology')..."
            className="advanced-negative-input"
          />
          <span className="text-[10px] text-slate-400 font-mono">Watertight 3D Geometry Filter Active</span>
        </div>
      )}

      {/* Main Glassmorphic Studio Prompt Dock */}
      <div className="studio-prompt-dock">
        {/* Left: Samples Catalog Button */}
        <button
          type="button"
          onClick={onOpenSamples}
          className="dock-samples-btn"
          title="Browse Curated 3D Model Prompt Catalog"
        >
          <Layers className="w-4 h-4 text-indigo-400" />
          <span className="hidden md:inline">Catalog</span>
        </button>

        <div className="dock-v-divider" />

        {/* Center: Sparkle + Input Box */}
        <div className="prompt-input-area">
          <Sparkles className="w-4 h-4 text-purple-400 shrink-0" />
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe any 3D asset (e.g. 'Futuristic cyber car', 'Damascus katana', 'Glowing crystal')..."
            className="prompt-main-input"
            disabled={isLoading}
          />
        </div>

        {/* Advanced Toggle Button */}
        <button
          type="button"
          onClick={() => setShowAdvanced((prev) => !prev)}
          className={`dock-advanced-toggle ${showAdvanced ? 'active' : ''}`}
          title="Toggle Negative Prompt & Advanced Generation Options"
        >
          <SlidersHorizontal className="w-3.5 h-3.5" />
          {showAdvanced ? (
            <ChevronDown className="w-3 h-3 opacity-70" />
          ) : (
            <ChevronUp className="w-3 h-3 opacity-70" />
          )}
        </button>

        {/* Right Controls: Style & Polycount */}
        <div className="dock-selectors-group">
          {/* Style Selector */}
          <select
            value={stylePreset}
            onChange={(e) => setStylePreset(e.target.value)}
            disabled={isLoading}
            className="dock-select-chip"
            title="PBR Texture Shader Style"
          >
            {STYLES.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>

          {/* Polycount Selector */}
          <div className="polycount-chip" title="Target Polygon Density">
            <Cpu className="w-3 h-3 text-cyan-400 shrink-0" />
            <select
              value={targetFaces}
              onChange={(e) => setTargetFaces(Number(e.target.value))}
              disabled={isLoading}
              className="dock-select-chip font-mono"
            >
              {POLY_PRESETS.map((n) => (
                <option key={n} value={n}>{(n / 1000)}k polys</option>
              ))}
            </select>
          </div>

          {/* Primary Action Button: Synthesize */}
          <button
            type="button"
            onClick={onGenerate}
            disabled={isLoading || !prompt.trim()}
            className={`dock-generate-btn ${prompt.trim() ? 'active' : ''}`}
            title="Synthesize 3D Model from Text (Press Enter)"
          >
            {isLoading ? (
              <div className="dock-btn-spinner" />
            ) : (
              <>
                <span className="font-semibold text-xs tracking-wide">Generate 3D</span>
                <ArrowUp className="w-3.5 h-3.5 stroke-[2.5]" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default PromptBar;
