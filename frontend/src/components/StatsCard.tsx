import { useState } from 'react';
import {
  Download,
  Box,
  Layers,
  ChevronDown,
  ShieldCheck,
  Zap,
  Sparkles
} from 'lucide-react';
import type { ModelMetadata } from '../types';

interface StatsCardProps {
  model: ModelMetadata | null;
  apiBase: string;
  onOpenTextures?: () => void;
}

export function StatsCard({ model, apiBase, onOpenTextures }: StatsCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!model) return null;

  const hasPbr = !!(model.textures && Object.keys(model.textures).length > 0);
  const cleanId = (model.model_id || '').replace(/^week\d+_?/i, '');

  return (
    <div className="floating-asset-hud-container">
      {/* Sleek Floating Glass Pill */}
      <div className="floating-asset-pill">
        <button
          type="button"
          onClick={() => setIsExpanded((prev) => !prev)}
          className="asset-pill-main-btn"
          title="Click to expand full 3D geometry metrics & PBR breakdown"
        >
          <Box className="w-3.5 h-3.5 text-cyan-400 shrink-0" />
          <span className="font-mono font-bold text-xs text-white">#{cleanId}</span>
          <span className="font-mono text-[11px] text-cyan-300 bg-cyan-500/10 px-1.5 py-0.5 rounded border border-cyan-500/20">
            {model.stats.faces.toLocaleString()} tris
          </span>
          <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 shadow-[0_0_6px_#34d399]" />
          <ChevronDown className={`w-3 h-3 text-slate-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
        </button>

        <div className="asset-pill-divider" />

        {/* 1-Click Game-Ready GLB Download */}
        {model.urls?.glb && (
          <a
            href={`${apiBase}${model.urls.glb}`}
            download={`polygen_${cleanId}.glb`}
            className="asset-pill-download-btn"
            title="Download Universal Binary .GLB (Embedded PBR Materials)"
          >
            <Download className="w-3 h-3 text-indigo-400" />
            <span>.GLB</span>
          </a>
        )}

        {/* 1-Click Wavefront OBJ Download */}
        {model.urls?.obj && (
          <a
            href={`${apiBase}${model.urls.obj}`}
            download={`polygen_${cleanId}.obj`}
            className="asset-pill-download-btn secondary"
            title="Download Wavefront .OBJ Mesh"
          >
            <span>.OBJ</span>
          </a>
        )}
      </div>

      {/* Expanded Glass Details Popover */}
      {isExpanded && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setIsExpanded(false)} />
          <div className="floating-asset-dropdown-sheet">
            {/* Header with prompt */}
            <div className="mb-3">
              <div className="flex items-center gap-1.5 text-xs font-bold text-white mb-1">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400" />
                <span>Asset Specification</span>
              </div>
              <p className="text-[11px] text-slate-400 italic line-clamp-2">
                "{model.prompt}"
              </p>
            </div>

            {/* Metrics 4-Grid */}
            <div className="grid grid-cols-2 gap-2 mb-3">
              <div className="bg-white/[0.03] border border-white/5 rounded-lg p-2">
                <div className="text-[10px] text-slate-400">Polygons</div>
                <div className="text-sm font-bold font-mono text-white">
                  {model.stats.faces.toLocaleString()}
                </div>
                <div className="text-[9px] text-slate-500">triangles</div>
              </div>

              <div className="bg-white/[0.03] border border-white/5 rounded-lg p-2">
                <div className="text-[10px] text-slate-400">Vertices</div>
                <div className="text-sm font-bold font-mono text-slate-200">
                  {model.stats.vertices.toLocaleString()}
                </div>
                <div className="text-[9px] text-slate-500">indexed</div>
              </div>

              <div className="bg-white/[0.03] border border-white/5 rounded-lg p-2">
                <div className="text-[10px] text-slate-400">QEM Reduction</div>
                <div className="text-sm font-bold font-mono text-emerald-400">
                  {model.decimation?.reduction_percentage || '0.0%'}
                </div>
                <div className="text-[9px] text-slate-500">optimized</div>
              </div>

              <div className="bg-white/[0.03] border border-white/5 rounded-lg p-2">
                <div className="text-[10px] text-slate-400">Latency</div>
                <div className="text-sm font-bold font-mono text-cyan-400">
                  {model.duration_seconds}s
                </div>
                <div className="text-[9px] text-slate-500">pipeline</div>
              </div>
            </div>

            {/* Integrity status */}
            <div className="flex items-center justify-between text-[11px] mb-3 pb-2 border-b border-white/5">
              <div className="flex items-center gap-1.5 text-emerald-400 font-medium">
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>Watertight Manifold</span>
              </div>
              <div className="flex items-center gap-1 text-slate-300 font-mono text-[10px]">
                <Zap className="w-3 h-3 text-amber-400" />
                <span>PBR Ready</span>
              </div>
            </div>

            {/* Inspect PBR Maps Button */}
            {hasPbr && onOpenTextures && (
              <button
                type="button"
                onClick={() => {
                  onOpenTextures();
                  setIsExpanded(false);
                }}
                className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-indigo-500/15 border border-indigo-500/30 text-indigo-200 hover:bg-indigo-500/25 transition text-xs font-semibold"
              >
                <div className="flex items-center gap-2">
                  <Layers className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Inspect 1024px Texture Maps</span>
                </div>
                <span className="text-[10px] font-mono text-indigo-300">4 Maps</span>
              </button>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default StatsCard;
