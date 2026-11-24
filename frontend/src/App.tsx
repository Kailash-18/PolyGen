import { useState, useEffect } from 'react';
import './App.css';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Scene3D } from './canvas/Scene3D';
import { PromptBar } from './components/PromptBar';
import { ProgressBar } from './components/ProgressBar';
import { StatsCard } from './components/StatsCard';
import { CanvasControls } from './components/CanvasControls';
import { LibraryView } from './components/LibraryView';
import { AuditView } from './components/AuditView';
import { LoginDashboard } from './components/LoginDashboard';
import { TexturePreviewModal } from './components/TexturePreviewModal';
import { BomDrawer } from './components/BomDrawer';
import { ViewportCustomizer } from './components/ViewportCustomizer';
import type { ModelMetadata, ProgressUpdate, ActiveTab, RenderMode, CameraPreset, ViewportSettings } from './types';

const API_BASE = 'http://localhost:8000';
const WS_BASE = 'ws://localhost:8000';

function AuthenticatedStudio() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('studio');
  const [prompt, setPrompt] = useState('A rusted medieval broadsword with a glowing blue sapphire in the hilt');
  const [targetFaces, setTargetFaces] = useState(10000);
  const [stylePreset, setStylePreset] = useState('Realistic PBR');
  const [isLoading, setIsLoading] = useState(false);
  const [progressData, setProgressData] = useState<ProgressUpdate | null>(null);
  const [activeModel, setActiveModel] = useState<ModelMetadata | null>(null);
  const [modelsList, setModelsList] = useState<ModelMetadata[]>([]);
  const [gpuInfo, setGpuInfo] = useState<{ cuda_available: boolean; device_name: string } | undefined>(undefined);

  // 3D Viewport Controls & Customization
  const [renderMode, setRenderMode] = useState<RenderMode>('pbr');
  const [autoRotate, setAutoRotate] = useState(false);
  const [lightIntensity, setLightIntensity] = useState(1.2);
  const [explodeProgress, setExplodeProgress] = useState(0);

  // Custom Studio Features
  const [viewportSettings, setViewportSettings] = useState<ViewportSettings>({
    showGrid: true,
    showShadows: true,
    clayColor: '#cbd5e1',
    wireframeColor: '#38bdf8',
    roughnessMultiplier: 1.0,
    metalnessMultiplier: 1.0
  });
  const [cameraPreset, setCameraPreset] = useState<CameraPreset>('default');
  const [resetTrigger, setResetTrigger] = useState(0);
  const [isCustomizerOpen, setIsCustomizerOpen] = useState(false);

  // Modals / Drawers
  const [textureModalModel, setTextureModalModel] = useState<ModelMetadata | null>(null);
  const [bomModalModelId, setBomModalModelId] = useState<string | null>(null);

  const handleCaptureSnapshot = () => {
    const canvas = document.querySelector('.scene-container canvas') as HTMLCanvasElement;
    if (!canvas) return;
    try {
      const dataUrl = canvas.toDataURL('image/png');
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = `polygen_${activeModel?.model_id || 'viewport'}_render.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    } catch (err) {
      console.warn('Could not capture canvas snapshot:', err);
    }
  };

  // Fetch initial health and library models on load
  const loadModels = () => {
    fetch(`${API_BASE}/api/models`)
      .then((res) => res.json())
      .then((data) => {
        if (data.models && Array.isArray(data.models)) {
          setModelsList(data.models);
          if (!activeModel && data.models.length > 0) {
            setActiveModel(data.models[0]);
          }
        }
      })
      .catch((err) => console.warn('Could not load models list:', err));
  };

  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data.gpu) setGpuInfo(data.gpu);
      })
      .catch((err) => console.warn('Backend not yet reachable on port 8000:', err));

    loadModels();
  }, []);

  const handleGenerate = () => {
    if (!prompt.trim() || isLoading) return;

    setIsLoading(true);
    setProgressData({
      step: 1,
      total_steps: 5,
      stage: 'Connecting',
      progress: 5,
      message: 'Connecting to PolyGen Multi-Stage AI Pipeline...'
    });

    try {
      const ws = new WebSocket(`${WS_BASE}/ws/generate`);

      ws.onopen = () => {
        ws.send(JSON.stringify({
          prompt: `${prompt.trim()} (${stylePreset})`,
          target_faces: targetFaces,
          detail_level: 'high'
        }));
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.error) {
          alert(`Generation error: ${data.error}`);
          setIsLoading(false);
          ws.close();
          return;
        }

        setProgressData(data);

        if (data.progress === 100 && data.result) {
          setActiveModel(data.result);
          setModelsList((prev) => [data.result, ...prev]);
          setIsLoading(false);
          ws.close();
        }
      };

      ws.onerror = (err) => {
        console.error('WebSocket connection error, falling back to HTTP:', err);
        fallbackHttpGenerate();
      };
    } catch {
      fallbackHttpGenerate();
    }
  };

  const fallbackHttpGenerate = async () => {
    try {
      setProgressData({
        step: 2,
        total_steps: 5,
        stage: 'Generating',
        progress: 40,
        message: 'Synthesizing 3D geometry & PBR texture maps...'
      });

      const res = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: `${prompt.trim()} (${stylePreset})`,
          target_faces: targetFaces,
          detail_level: 'high'
        })
      });

      if (!res.ok) throw new Error('API request failed');
      const data: ModelMetadata = await res.json();

      setActiveModel(data);
      setModelsList((prev) => [data, ...prev]);
      setProgressData({
        step: 5,
        total_steps: 5,
        stage: 'Complete',
        progress: 100,
        message: '3D Asset ready with PBR textures!',
        result: data
      });
    } catch (err: any) {
      alert(`Generation failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteModel = async (id: string) => {
    if (!confirm(`Are you sure you want to delete asset ${id}?`)) return;
    try {
      await fetch(`${API_BASE}/api/models/${id}`, { method: 'DELETE' });
      setModelsList((prev) => prev.filter((m) => m.model_id !== id));
      if (activeModel?.model_id === id) {
        setActiveModel(null);
      }
    } catch (err) {
      console.error('Failed to delete model:', err);
    }
  };

  const currentGlbUrl = activeModel ? `${API_BASE}${activeModel.urls.glb}` : null;
  const hasTextures = !!(activeModel?.textures && Object.keys(activeModel.textures).length > 0);

  return (
    <div className="app-container">
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        gpuInfo={gpuInfo}
      />

      <main className="workspace-layout">
        {activeTab === 'studio' && (
          <section className="viewport-area">
            <CanvasControls
              renderMode={renderMode}
              setRenderMode={setRenderMode}
              autoRotate={autoRotate}
              setAutoRotate={setAutoRotate}
              lightIntensity={lightIntensity}
              setLightIntensity={setLightIntensity}
              hasTextures={hasTextures}
              onOpenTextures={() => setTextureModalModel(activeModel)}
              explodeProgress={explodeProgress}
              setExplodeProgress={setExplodeProgress}
              onOpenBom={() => {
                if (activeModel) setBomModalModelId(activeModel.model_id);
              }}
              onToggleCustomizer={() => setIsCustomizerOpen((prev) => !prev)}
              isCustomizerOpen={isCustomizerOpen}
              onCaptureSnapshot={handleCaptureSnapshot}
            />

            <Scene3D
              modelUrl={currentGlbUrl}
              renderMode={renderMode}
              autoRotate={autoRotate}
              lightIntensity={lightIntensity}
              explodeProgress={explodeProgress}
              settings={viewportSettings}
              cameraPreset={cameraPreset}
              resetTrigger={resetTrigger}
            />

            <ViewportCustomizer
              isOpen={isCustomizerOpen}
              onClose={() => setIsCustomizerOpen(false)}
              settings={viewportSettings}
              setSettings={setViewportSettings}
              cameraPreset={cameraPreset}
              setCameraPreset={setCameraPreset}
              onResetCamera={() => {
                setCameraPreset('default');
                setResetTrigger((prev) => prev + 1);
              }}
            />

            <ProgressBar progressData={progressData} />

            <StatsCard
              model={activeModel}
              apiBase={API_BASE}
              onOpenTextures={() => setTextureModalModel(activeModel)}
            />

            <PromptBar
              prompt={prompt}
              setPrompt={setPrompt}
              targetFaces={targetFaces}
              setTargetFaces={setTargetFaces}
              stylePreset={stylePreset}
              setStylePreset={setStylePreset}
              onGenerate={handleGenerate}
              isLoading={isLoading}
            />
          </section>
        )}

        {activeTab === 'library' && (
          <LibraryView
            models={modelsList}
            apiBase={API_BASE}
            onSelectModel={(m) => {
              setActiveModel(m);
              setActiveTab('studio');
            }}
            onDeleteModel={handleDeleteModel}
            onOpenTextures={(m) => setTextureModalModel(m)}
            onGoToStudio={() => setActiveTab('studio')}
          />
        )}

        {activeTab === 'audit' && (
          <AuditView models={modelsList} gpuInfo={gpuInfo} />
        )}
      </main>

      {textureModalModel && textureModalModel.textures && (
        <TexturePreviewModal
          modelId={textureModalModel.model_id}
          textures={textureModalModel.textures}
          apiBase={API_BASE}
          onClose={() => setTextureModalModel(null)}
        />
      )}

      {bomModalModelId && (
        <BomDrawer
          modelId={bomModalModelId}
          apiBase={API_BASE}
          onClose={() => setBomModalModelId(null)}
        />
      )}
    </div>
  );
}

function RootApp() {
  const { isLoggedIn, user } = useAuth();

  if (!isLoggedIn || !user) {
    return <LoginDashboard />;
  }

  return <AuthenticatedStudio />;
}

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <RootApp />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
