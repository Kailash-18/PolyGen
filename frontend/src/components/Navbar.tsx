import { Box, Cpu, Code2 } from 'lucide-react';

interface NavbarProps {
  gpuInfo?: {
    cuda_available: boolean;
    device_name: string;
  };
}

export function Navbar({ gpuInfo }: NavbarProps) {
  return (
    <header className="navbar">
      <div className="nav-brand">
        <div className="nav-logo">
          <Box className="w-6 h-6 text-purple-400" />
        </div>
        <div>
          <div className="brand-title">
            <span>Poly</span><span className="brand-accent">Gen</span>
            <span className="badge-week">Week 1: Canvas & Mesh Engine</span>
          </div>
          <p className="brand-sub">Generative Text-to-3D Asset Pipeline</p>
        </div>
      </div>

      <div className="nav-actions">
        <a
          href="http://localhost:8000/viewer/"
          target="_blank"
          rel="noreferrer"
          className="viewer-launch-btn"
          title="Open Full 3D Exploded-View & Kinematics Studio"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '6px 14px',
            borderRadius: '8px',
            background: 'linear-gradient(135deg, #0ea5e9, #a855f7)',
            color: '#fff',
            fontWeight: 600,
            fontSize: '13px',
            textDecoration: 'none',
            boxShadow: '0 2px 10px rgba(14, 165, 233, 0.35)'
          }}
        >
          <Box className="w-4 h-4" />
          <span>3D Studio Viewer</span>
        </a>

        <div className="gpu-badge">
          <Cpu className="w-4 h-4 text-emerald-400" />
          <span>{gpuInfo?.cuda_available ? gpuInfo.device_name : 'Local Engine Ready'}</span>
        </div>

        <a
          href="https://github.com/Kailash-18/PolyGen"
          target="_blank"
          rel="noreferrer"
          className="github-btn"
        >
          <Code2 className="w-4 h-4" />
          <span>GitHub</span>
        </a>
      </div>
    </header>
  );
}
