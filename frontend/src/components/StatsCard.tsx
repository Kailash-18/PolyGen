import { Download, Zap } from 'lucide-react';
import type { ModelMetadata } from '../types';

interface StatsCardProps {
  model: ModelMetadata | null;
  apiBase: string;
}

export function StatsCard({ model, apiBase }: StatsCardProps) {
  if (!model) return null;

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
          <span className="stat-sub">Multi-stage pipeline</span>
        </div>
      </div>

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
