import { Download, Zap, Layers, Sparkles } from 'lucide-react';
import type { ModelMetadata } from '../types';

interface StatsCardProps {
  model: ModelMetadata | null;
  apiBase: string;
  onOpenTextures?: () => void;
}

export function StatsCard({ model, apiBase, onOpenTextures }: StatsCardProps) {
  if (!model) return null;

  const hasPbr = model.textures && Object.keys(model.textures).length > 0;

  return (
    <div className="stats-card">
      <div className="stats-header">
        <div className="flex items-center gap-2">
          <Zap className="w-4 h-4 text-amber-400" />
          <span className="stats-title">Generated Asset Specs</span>
        </div>
        <span className="model-badge">ID: {model.model_id}</span>
      </div>

      <div className="stats-grid">
        <div className="stat-box">
          <span className="stat-label">Faces (Polygons)</span>
          <span className="stat-value text-purple-400">
            {model.stats.faces.toLocaleString()}
          </span>
          <span className="stat-sub">
            from {model.decimation.before_faces.toLocaleString()}
          </span>
        </div>

        <div className="stat-box">
          <span className="stat-label">Vertices</span>
          <span className="stat-value">
            {model.stats.vertices.toLocaleString()}
          </span>
          <span className="stat-sub">Cleaned & indexed</span>
        </div>

        <div className="stat-box">
          <span className="stat-label">Optimization</span>
          <span className="stat-value text-emerald-400">
            {model.decimation.reduction_percentage}
          </span>
          <span className="stat-sub">QEM reduction</span>
        </div>

        <div className="stat-box">
          <span className="stat-label">Generation Time</span>
          <span className="stat-value text-sky-400">
            {model.duration_seconds}s
          </span>
          <span className="stat-sub">5-stage pipeline</span>
        </div>
      </div>

      {/* PBR Texture Info Tag */}
      {hasPbr && (
        <div className="pbr-status-box">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-3.5 h-3.5 text-purple-400" />
              <span className="text-xs font-semibold text-slate-200">
                PBR Maps: 1024px Albedo + Normal + Roughness
              </span>
            </div>
            {onOpenTextures && (
              <button
                onClick={onOpenTextures}
                className="text-xs text-purple-400 hover:text-purple-300 font-medium underline flex items-center gap-1"
              >
                <Layers className="w-3 h-3" />
                <span>View Maps</span>
              </button>
            )}
          </div>
        </div>
      )}

      <div className="stats-footer">
        <a
          href={`${apiBase}${model.urls.glb}`}
          download={`polygen_${model.model_id}.glb`}
          className="download-btn btn-primary"
        >
          <Download className="w-4 h-4" />
          <span>Download .GLB (Game-Ready)</span>
        </a>

        <a
          href={`${apiBase}${model.urls.obj}`}
          download={`polygen_${model.model_id}.obj`}
          className="download-btn btn-secondary"
        >
          <Download className="w-4 h-4" />
          <span>Download .OBJ (Raw Mesh)</span>
        </a>
      </div>
    </div>
  );
}
