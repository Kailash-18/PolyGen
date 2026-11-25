import { useState } from 'react';
import { X, ArrowUpRight, Sparkles } from 'lucide-react';

export interface SampleItem {
  id: string;
  name: string;
  category: 'Weapons' | 'Armor' | 'Archaeology' | 'Industrial' | 'Sci-Fi';
  prompt: string;
  style: string;
  faces: number;
  vertices: number;
  decimation: string;
  maps: string[];
  gradient: string;
  icon: string;
}

export const SAMPLE_CATALOG: SampleItem[] = [
  {
    id: 'sample_broadsword',
    name: 'Rusted Medieval Broadsword',
    category: 'Weapons',
    prompt: 'A rusted medieval broadsword with a glowing blue sapphire in the hilt and weathered crossguard',
    style: 'Realistic PBR',
    faces: 7296,
    vertices: 3652,
    decimation: '85.4%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-amber-500/20 to-purple-500/20',
    icon: '⚔️'
  },
  {
    id: 'sample_shield',
    name: 'Knight Tower Shield',
    category: 'Armor',
    prompt: 'A heavy knight tower shield with reinforced iron boss, curved oak planks, and heraldic crest',
    style: 'Realistic PBR',
    faces: 6840,
    vertices: 3422,
    decimation: '86.2%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-blue-500/20 to-slate-500/20',
    icon: '🛡️'
  },
  {
    id: 'sample_vase',
    name: 'Corinthian Amphora Vase',
    category: 'Archaeology',
    prompt: 'An ancient ceramic Greek amphora vase with etched mythological meanders and terracotta patina',
    style: 'Antique',
    faces: 5120,
    vertices: 2562,
    decimation: '89.7%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-orange-500/20 to-amber-500/20',
    icon: '🏺'
  },
  {
    id: 'sample_chair',
    name: 'Ergonomic Task Chair',
    category: 'Industrial',
    prompt: 'A modern ergonomic office task chair with breathable lumbar mesh and polished aluminum base',
    style: 'Low Poly CAD',
    faces: 8450,
    vertices: 4228,
    decimation: '83.1%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-emerald-500/20 to-teal-500/20',
    icon: '🪑'
  },
  {
    id: 'sample_crystal',
    name: 'Obsidian Hex-Crystal Cluster',
    category: 'Sci-Fi',
    prompt: 'A glowing hexagonal crystal cluster with obsidian bedrock and bismuth violet refraction',
    style: 'Sci-Fi Cyber',
    faces: 4200,
    vertices: 2102,
    decimation: '91.6%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-violet-500/20 to-fuchsia-500/20',
    icon: '💎'
  },
  {
    id: 'sample_drone',
    name: 'Autonomous Recon Drone',
    category: 'Industrial',
    prompt: 'A compact tactical quadcopter drone with matte titanium fuselage and optical sensor dome',
    style: 'Sci-Fi Cyber',
    faces: 9180,
    vertices: 4594,
    decimation: '81.6%',
    maps: ['Albedo', 'Normal', 'Roughness'],
    gradient: 'from-cyan-500/20 to-sky-500/20',
    icon: '🛸'
  }
];

interface SampleModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectSample: (sample: SampleItem) => void;
}

export function SampleModal({ isOpen, onClose, onSelectSample }: SampleModalProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [activeId, setActiveId] = useState<string | null>(null);

  if (!isOpen) return null;

  const categories = ['All', 'Weapons', 'Armor', 'Archaeology', 'Industrial', 'Sci-Fi'];

  const filtered = selectedCategory === 'All'
    ? SAMPLE_CATALOG
    : SAMPLE_CATALOG.filter((s) => s.category === selectedCategory);

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="sample-modal-container" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="sample-modal-header">
          <div className="flex items-center gap-2">
            <div className="sample-header-icon">
              <Sparkles className="w-4 h-4 text-purple-400" />
            </div>
            <div>
              <h2 className="sample-modal-title">3D Asset Sample Library</h2>
              <p className="sample-modal-sub">
                Select a verified production asset to test geometry, PBR maps, and QEM decimation
              </p>
            </div>
          </div>
          <button type="button" onClick={onClose} className="modal-close-btn" title="Close">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Category Tabs */}
        <div className="sample-category-row">
          {categories.map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setSelectedCategory(cat)}
              className={`sample-cat-pill ${selectedCategory === cat ? 'active' : ''}`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* 3D Sample Cards Grid */}
        <div className="sample-cards-grid">
          {filtered.map((item) => (
            <div
              key={item.id}
              className={`sample-catalog-card ${activeId === item.id ? 'selected' : ''}`}
              onClick={() => setActiveId(item.id)}
            >
              <div className="sample-card-visual">
                <span className="sample-card-emoji">{item.icon}</span>
                <span className="sample-card-badge">{item.category}</span>
              </div>

              <div className="sample-card-body">
                <h3 className="sample-card-name">{item.name}</h3>
                <p className="sample-card-prompt">"{item.prompt}"</p>

                {/* Specs row */}
                <div className="sample-card-specs">
                  <div className="spec-unit">
                    <span className="spec-unit-label">Polygons</span>
                    <span className="spec-unit-val font-mono">{item.faces.toLocaleString()}</span>
                  </div>
                  <div className="spec-unit">
                    <span className="spec-unit-label">QEM Decim</span>
                    <span className="spec-unit-val text-emerald-400 font-mono">{item.decimation}</span>
                  </div>
                  <div className="spec-unit">
                    <span className="spec-unit-label">PBR Maps</span>
                    <span className="spec-unit-val text-purple-400">3x 1024px</span>
                  </div>
                </div>

                {/* Action button */}
                <button
                  type="button"
                  onClick={() => {
                    onSelectSample(item);
                    onClose();
                  }}
                  className="sample-load-action"
                >
                  <span>Load Into Studio</span>
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
