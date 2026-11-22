import { useState } from 'react';
import {
  FolderOpen,
  Search,
  Download,
  Trash2,
  Box,
  Layers,
  Sparkles,
  ArrowUpRight
} from 'lucide-react';
import type { ModelMetadata } from '../types';

interface LibraryViewProps {
  models: ModelMetadata[];
  apiBase: string;
  onSelectModel: (m: ModelMetadata) => void;
  onDeleteModel: (id: string) => void;
  onOpenTextures: (m: ModelMetadata) => void;
  onGoToStudio: () => void;
}

export function LibraryView({
  models,
  apiBase,
  onSelectModel,
  onDeleteModel,
  onOpenTextures,
  onGoToStudio
}: LibraryViewProps) {
  const [search, setSearch] = useState('');

  const filtered = models.filter((m) =>
    m.prompt.toLowerCase().includes(search.toLowerCase()) ||
    m.model_id.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="library-view-container">
      <div className="library-header-row">
        <div>
          <h2 className="library-title">3D Asset Library & Projects</h2>
          <p className="library-subtitle">
            Manage, inspect, and export your AI-generated 3D game assets ({models.length} assets)
          </p>
        </div>

        <div className="library-actions-row">
          <div className="search-box">
            <Search className="w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search assets by prompt or ID..."
              className="search-input"
            />
          </div>

          <button onClick={onGoToStudio} className="new-asset-btn">
            <Sparkles className="w-4 h-4" />
            <span>New Generation</span>
          </button>
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="empty-library-card">
          <div className="empty-icon-box">
            <FolderOpen className="w-10 h-10 text-purple-400" />
          </div>
          <h3 className="empty-title">No 3D Assets Found</h3>
          <p className="empty-desc">
            {search
              ? `No models matching "${search}". Try another search term.`
              : 'You have not generated any 3D models yet. Head over to the studio to build your first model!'}
          </p>
          <button onClick={onGoToStudio} className="generate-btn mt-4">
            <Sparkles className="w-4 h-4" />
            <span>Go to 3D Studio</span>
          </button>
        </div>
      ) : (
        <div className="library-grid">
          {filtered.map((item) => (
            <div key={item.model_id} className="asset-card">
              <div className="asset-card-top">
                <div className="flex items-center gap-2">
                  <div className="asset-icon">
                    <Box className="w-4 h-4 text-purple-400" />
                  </div>
                  <span className="asset-id">ID: {item.model_id}</span>
                </div>
                <span className="asset-date">{item.created_at || 'Recent'}</span>
              </div>

              {/* Prompt */}
              <h4 className="asset-prompt" title={item.prompt}>
                "{item.prompt}"
              </h4>

              {/* Metric stats */}
              <div className="asset-metrics">
                <div className="metric-pill">
                  <span className="metric-label">Polygons:</span>
                  <span className="metric-val">{item.stats.faces.toLocaleString()}</span>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">Reduction:</span>
                  <span className="metric-val text-emerald-400">
                    {item.decimation.reduction_percentage}
                  </span>
                </div>
                <div className="metric-pill">
                  <span className="metric-label">Latency:</span>
                  <span className="metric-val text-sky-400">{item.duration_seconds}s</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="asset-actions">
                <button
                  onClick={() => onSelectModel(item)}
                  className="asset-action-btn btn-view"
                  title="Load and inspect in 3D canvas"
                >
                  <ArrowUpRight className="w-3.5 h-3.5" />
                  <span>Open in Studio</span>
                </button>

                {item.textures && (
                  <button
                    onClick={() => onOpenTextures(item)}
                    className="asset-action-btn btn-textures"
                    title="Inspect PBR texture atlas"
                  >
                    <Layers className="w-3.5 h-3.5" />
                    <span>PBR Maps</span>
                  </button>
                )}

                <a
                  href={`${apiBase}${item.urls.glb}`}
                  download={`polygen_${item.model_id}.glb`}
                  className="asset-action-btn btn-dl"
                  title="Download binary .GLB file"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>.GLB</span>
                </a>

                <button
                  onClick={() => onDeleteModel(item.model_id)}
                  className="asset-action-btn btn-del"
                  title="Delete asset"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
