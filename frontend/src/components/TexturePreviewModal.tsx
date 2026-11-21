import { X, Layers, Image as ImageIcon } from 'lucide-react';

interface TexturePreviewModalProps {
  modelId: string;
  textures: {
    albedo?: string;
    normal?: string;
    roughness?: string;
  };
  apiBase: string;
  onClose: () => void;
}

export function TexturePreviewModal({
  modelId,
  textures,
  apiBase,
  onClose
}: TexturePreviewModalProps) {
  const mapItems = [
    { name: 'Albedo / Diffuse Map', key: 'albedo', desc: 'Base surface color & detail' },
    { name: 'Normal Map (Tangent Space)', key: 'normal', desc: 'Surface relief & micro-normals' },
    { name: 'Roughness Map', key: 'roughness', desc: 'Specular reflections & glossiness' }
  ];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="texture-modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="texture-modal-header">
          <div className="flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-400" />
            <h3 className="text-lg font-semibold text-slate-100">
              PBR Texture Atlas Inspector
            </h3>
            <span className="model-badge">Asset ID: {modelId}</span>
          </div>
          <button className="modal-close-btn" onClick={onClose} aria-label="Close">
            <X className="w-5 h-5" />
          </button>
        </div>

        <p className="text-xs text-slate-400 mb-4">
          Generated via Stable Diffusion & ControlNet multi-pass UV projection. 1024x1024 seamless maps.
        </p>

        <div className="texture-grid">
          {mapItems.map((item) => {
            const url = textures[item.key as keyof typeof textures];
            const fullUrl = url ? `${apiBase}${url}` : null;

            return (
              <div key={item.key} className="texture-card">
                <div className="texture-img-box">
                  {fullUrl ? (
                    <img
                      src={fullUrl}
                      alt={item.name}
                      className="texture-preview-img"
                    />
                  ) : (
                    <div className="texture-placeholder">
                      <ImageIcon className="w-8 h-8 text-slate-500 mb-2" />
                      <span className="text-xs text-slate-400">Map generating...</span>
                    </div>
                  )}
                </div>
                <div className="texture-info">
                  <span className="texture-name">{item.name}</span>
                  <span className="texture-desc">{item.desc}</span>
                  {fullUrl && (
                    <a
                      href={fullUrl}
                      download={`${modelId}_${item.key}.png`}
                      className="texture-dl-link"
                    >
                      Download PNG
                    </a>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
