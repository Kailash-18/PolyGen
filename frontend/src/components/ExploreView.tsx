import { useState } from 'react';
import {
  Sparkles,
  Copy,
  Check,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck,
  Wand2
} from 'lucide-react';

export interface PromptShowcaseItem {
  id: string;
  title: string;
  category: 'Vehicles' | 'Weapons' | 'Sci-Fi' | 'Mechs' | 'Artifacts' | 'Props';
  prompt: string;
  style: string;
  targetFaces: number;
  tags: string[];
  icon: string;
  accentColor: string;
}

export const SHOWCASE_PROMPTS: PromptShowcaseItem[] = [
  {
    id: 'cyber-hypercar',
    title: 'Cyberpunk Hypercar',
    category: 'Vehicles',
    prompt: 'A sleek aerodynamic futuristic sports car with glowing neon rims, active carbon aero splitters, and quad titanium exhausts',
    style: 'Sci-Fi Cyber',
    targetFaces: 10000,
    tags: ['Watertight', 'PBR Shaded', 'Aerodynamic'],
    icon: '🏎️',
    accentColor: '#38bdf8'
  },
  {
    id: 'damascus-katana',
    title: 'Damascus Steel Katana',
    category: 'Weapons',
    prompt: 'A masterwork Japanese katana with folded Damascus steel blade, golden dragon tsuba guard, and silk-wrapped rayskin tsuka handle',
    style: 'Realistic PBR',
    targetFaces: 10000,
    tags: ['Game-Ready', 'PBR Metallic', 'High-Normal'],
    icon: '⚔️',
    accentColor: '#818cf8'
  },
  {
    id: 'orbital-starfighter',
    title: 'Orbital Interceptor Starfighter',
    category: 'Sci-Fi',
    prompt: 'A sci-fi starfighter spaceship with swept delta wings, dual plasma ion thrusters, and matte stealth cockpit canopy',
    style: 'Sci-Fi Cyber',
    targetFaces: 12000,
    tags: ['Low-Drag', 'Emissive Thrusters', 'Watertight'],
    icon: '🚀',
    accentColor: '#a855f7'
  },
  {
    id: 'heavy-mech',
    title: 'Titan Siege Mech',
    category: 'Mechs',
    prompt: 'A heavy bipedal combat mech with shoulder missile pods, reinforced knee actuators, and dual rotary plasma miniguns',
    style: 'Sci-Fi Cyber',
    targetFaces: 15000,
    tags: ['Multi-Part', 'Kinematic Rigged', 'PBR Armor'],
    icon: '🤖',
    accentColor: '#f59e0b'
  },
  {
    id: 'mana-crystal-cluster',
    title: 'Astral Mana Crystal',
    category: 'Artifacts',
    prompt: 'A cluster of glowing prismatic quartz mana crystals on dark basalt bedrock with ethereal violet bioluminescence',
    style: 'Sci-Fi Cyber',
    targetFaces: 6000,
    tags: ['Prismatic Specular', 'Volumetric Glow', 'Low-Poly'],
    icon: '💎',
    accentColor: '#ec4899'
  },
  {
    id: 'viking-war-axe',
    title: 'Nordic Runed Battleaxe',
    category: 'Weapons',
    prompt: 'A bearded Viking battleaxe with etched elder Futhark runes along the bearded blade, bronze collar, and cross-stitched leather haft',
    style: 'Antique Bronze',
    targetFaces: 8500,
    tags: ['Weathered PBR', 'Micro-Scratches', 'Historical'],
    icon: '🪓',
    accentColor: '#f97316'
  },
  {
    id: 'elixir-flask',
    title: 'Archmage Healing Elixir',
    category: 'Props',
    prompt: 'A teardrop alchemical potion flask with glowing ruby healing elixir, brass filigree filature cage, and wax-sealed cork',
    style: 'Realistic PBR',
    targetFaces: 5000,
    tags: ['Refraction', 'Subsurface Glow', 'Game Prop'],
    icon: '🧪',
    accentColor: '#ef4444'
  },
  {
    id: 'ancient-coffer',
    title: 'Gilded Dungeon Coffer',
    category: 'Artifacts',
    prompt: 'An ornate pirate treasure chest with wrought-iron banding, carved oak staves, lion-head handles, and brass lock plate',
    style: 'Realistic PBR',
    targetFaces: 9000,
    tags: ['Watertight', 'BOM Decomposable', 'PBR Wood & Metal'],
    icon: '📦',
    accentColor: '#eab308'
  },
  {
    id: 'plasma-rifle',
    title: 'Pulse Plasma Blaster',
    category: 'Weapons',
    prompt: 'A futuristic heavy plasma blaster with glowing cyan heat sinks, top tactical holo-sight, and textured polymer grip',
    style: 'Sci-Fi Cyber',
    targetFaces: 11000,
    tags: ['Sci-Fi FPS', 'Emissive Channels', 'Ergonomic'],
    icon: '🔫',
    accentColor: '#06b6d4'
  },
  {
    id: 'greek-amphora',
    title: 'Athenian Black-Figure Amphora',
    category: 'Props',
    prompt: 'An ancient Greek terracotta amphora vase with fluted neck, twin loop handles, and mythological Greek warrior frieze',
    style: 'Antique Bronze',
    targetFaces: 6500,
    tags: ['Archaeological', 'Terracotta PBR', 'Museum Grade'],
    icon: '🏺',
    accentColor: '#d97706'
  },
  {
    id: 'tactical-drone',
    title: 'Surveillance Hexacopter',
    category: 'Vehicles',
    prompt: 'A tactical military surveillance drone with folding carbon-fiber arms, spherical gimbal optical sensor dome, and LED navigation pods',
    style: 'Realistic PBR',
    targetFaces: 10500,
    tags: ['Aerospace', 'Carbon Weave', 'High-Poly'],
    icon: '🛸',
    accentColor: '#10b981'
  },
  {
    id: 'war-hammer',
    title: 'Dwarven Crag Hammer',
    category: 'Weapons',
    prompt: 'A massive dwarven war hammer with dual-sided steel striking faces, rear armor-piercing spike, and rune-chiseled granite core',
    style: 'Realistic PBR',
    targetFaces: 8000,
    tags: ['Heavy Impact', 'Chiseled Stone', 'PBR Steel'],
    icon: '🔨',
    accentColor: '#64748b'
  }
];

interface ExploreViewProps {
  onSelectPrompt: (prompt: string, style: string, faces: number) => void;
}

export function ExploreView({ onSelectPrompt }: ExploreViewProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const categories = ['All', 'Vehicles', 'Weapons', 'Sci-Fi', 'Mechs', 'Artifacts', 'Props'];

  const filtered = selectedCategory === 'All'
    ? SHOWCASE_PROMPTS
    : SHOWCASE_PROMPTS.filter((item) => item.category === selectedCategory);

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="explore-view-container">
      {/* Hero Header */}
      <div className="explore-hero-banner">
        <div className="explore-badge">
          <Sparkles className="w-3.5 h-3.5 text-amber-400" />
          <span>Curated Text-to-3D Prompt Showcase</span>
        </div>
        <h1 className="explore-hero-title">
          Explore Generative 3D Prompts
        </h1>
        <p className="explore-hero-subtitle">
          Discover verified text prompts engineered for high-fidelity 3D geometry, clean manifold topology, and multi-layer PBR textures. Click any card to immediately synthesize in the 3D Studio.
        </p>

        {/* Category Pills */}
        <div className="explore-categories-bar">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setSelectedCategory(cat)}
              className={`explore-cat-pill ${selectedCategory === cat ? 'active' : ''}`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Prompts Showcase Grid */}
      <div className="explore-cards-grid">
        {filtered.map((item) => (
          <div key={item.id} className="explore-card">
            {/* Card Top */}
            <div className="explore-card-top">
              <div className="flex items-center gap-2">
                <span className="text-xl" role="img" aria-label={item.title}>
                  {item.icon}
                </span>
                <div>
                  <h3 className="explore-card-title">{item.title}</h3>
                  <span className="explore-card-cat">{item.category}</span>
                </div>
              </div>

              <button
                type="button"
                onClick={() => handleCopy(item.id, item.prompt)}
                className="explore-copy-btn"
                title="Copy prompt to clipboard"
              >
                {copiedId === item.id ? (
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                ) : (
                  <Copy className="w-3.5 h-3.5 text-slate-400" />
                )}
              </button>
            </div>

            {/* Prompt Text Box */}
            <div className="explore-prompt-box">
              <p className="explore-prompt-text">
                "{item.prompt}"
              </p>
            </div>

            {/* Tags & Metadata */}
            <div className="explore-card-meta">
              <div className="flex items-center gap-1.5 text-[11px] font-mono text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20">
                <Layers className="w-3 h-3" />
                <span>{item.style}</span>
              </div>
              <div className="flex items-center gap-1.5 text-[11px] font-mono text-cyan-300 bg-cyan-500/10 px-2 py-0.5 rounded-md border border-cyan-500/20">
                <Cpu className="w-3 h-3" />
                <span>{item.targetFaces / 1000}k tris</span>
              </div>
              <div className="flex items-center gap-1 text-[11px] font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20 ml-auto">
                <ShieldCheck className="w-3 h-3" />
                <span>Watertight</span>
              </div>
            </div>

            {/* Primary Action Button: Synthesize */}
            <button
              type="button"
              onClick={() => onSelectPrompt(item.prompt, item.style, item.targetFaces)}
              className="explore-synthesize-btn"
            >
              <Wand2 className="w-3.5 h-3.5" />
              <span>Synthesize in 3D Studio</span>
              <ArrowRight className="w-3.5 h-3.5 ml-auto" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ExploreView;
