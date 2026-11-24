import { useState } from 'react';
import { Download, Box, Layers, ChevronDown, ChevronUp } from 'lucide-react';
import type { ModelMetadata } from '../types';

interface StatsCardProps {
  model: ModelMetadata | null;
  apiBase: string;
  onOpenTextures?: () => void;
}

export function StatsCard({ model, apiBase, onOpenTextures }: StatsCardProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);

  if (!model) return null;

  const hasPbr = model.textures && Object.keys(model.textures).length > 0;

  if (isCollapsed) {
    return (
      <button
        type="button"
        onClick={() => setIsCollapsed(false)}
        className="clean-stats-pill"
        title="Expand Telemetry Specs"
      >
        <Box className="w-3.5 h-3.5 text-purple-400" />
        <span className="font-semibold text-xs text-slate-200">#{model.model_id}</span>
        <span className="clean-stats-pill-metric">{model.stats.faces.toLocaleString()} polys</span>
        <ChevronDown className="w-3.5 h-3.5 opacity-60 ml-0.5" />
      </button>
    );
  }

  return (
    <div className="clean-stats-card">
      {/* Header */}
      <div className="clean-stats-header">
        <div className="clean-stats-header-left">
          <Box className="w-3.5 h-3.5 text-purple-400" />
          <span className="clean-stats-title">Asset Specs</span>
          <span className="clean-model-chip">#{model.model_id}</span>
        </div>
        <button
          type="button"
          onClick={() => setIsCollapsed(true)}
          className="clean-collapse-btn"
          title="Minimize Specs Card"
        >
          <ChevronUp className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* 4-Box Telemetry Grid */}
      <div className="clean-specs-grid">
        <div className="clean-spec-box">
          <span className="spec-label">Faces</span>
          <span className="spec-value text-slate-100 font-mono">
            {model.stats.faces.toLocaleString()}
          </span>
          <span className="spec-sub">orig: {model.decimation.before_faces.toLocaleString()}</span>
        </div>

        <div className="clean-spec-box">
          <span className="spec-label">Vertices</span>
          <span className="spec-value text-slate-200 font-mono">
            {model.stats.vertices.toLocaleString()}
          </span>
          <span className="spec-sub">Cleaned & indexed</span>
        </div>

        <div className="clean-spec-box">
          <span className="spec-label">Decimation</span>
          <span className="spec-value text-emerald-400 font-mono">
            {model.decimation.reduction_percentage}
          </span>
          <span className="spec-sub">QEM topology</span>
        </div>

        <div className="clean-spec-box">
          <span className="spec-label">Synthesis</span>
          <span className="spec-value text-sky-400 font-mono">
            {model.duration_seconds}s
          </span>
          <span className="spec-sub">5-stage pipeline</span>
        </div>
      </div>

      {/* PBR Texture Info Tag */}
      {hasPbr && (
        <div className="clean-pbr-box">
          <div className="clean-pbr-row">
            <div className="flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-purple-400" />
              <span className="text-xs font-semibold text-slate-200">1024px PBR Maps</span>
            </div>
            {onOpenTextures && (
              <button
                type="button"
                onClick={onOpenTextures}
                className="clean-inspect-pill"
              >
                <Layers className="w-3 h-3" />
                <span>Inspect</span>
              </button>
            )}
          </div>
          <div className="clean-pbr-chips">
            <span className="pbr-chip">Albedo</span>
            <span className="pbr-chip">Normal</span>
            <span className="pbr-chip">Roughness</span>
          </div>
        </div>
      )}

      {/* Downloads */}
      <div className="clean-stats-actions">
        <a
          href={`${apiBase}${model.urls.glb}`}
          download={`polygen_${model.model_id}.glb`}
          className="clean-download-primary"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export .GLB (Game-Ready)</span>
        </a>

        <a
          href={`${apiBase}${model.urls.obj}`}
          download={`polygen_${model.model_id}.obj`}
          className="clean-download-secondary"
        >
          <Box className="w-3.5 h-3.5 text-slate-400" />
          <span>Export .OBJ (Raw Mesh)</span>
        </a>
      </div>
    </div>
  );
}
