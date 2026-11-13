import { useState, useEffect } from 'react';
import './App.css';
import { Navbar } from './components/Navbar';
import { Scene3D } from './canvas/Scene3D';
import { PromptBar } from './components/PromptBar';
import { ProgressBar } from './components/ProgressBar';
import { StatsCard } from './components/StatsCard';
import { CanvasControls } from './components/CanvasControls';
import type { ModelMetadata, ProgressUpdate } from './types';

const API_BASE = 'http://localhost:8000';
const WS_BASE = 'ws://localhost:8000';

export function App() {
  const [prompt, setPrompt] = useState('A rusted medieval broadsword with a glowing blue sapphire in the hilt');
  const [targetFaces, setTargetFaces] = useState(10000);
  const [isLoading, setIsLoading] = useState(false);
  const [progressData, setProgressData] = useState<ProgressUpdate | null>(null);
  const [activeModel, setActiveModel] = useState<ModelMetadata | null>(null);
  const [gpuInfo, setGpuInfo] = useState<{ cuda_available: boolean; device_name: string } | undefined>(undefined);

  // 3D Canvas Settings
  const [wireframe, setWireframe] = useState(false);
  const [autoRotate, setAutoRotate] = useState(true);
  const [lightIntensity, setLightIntensity] = useState(1.2);

  // Check backend health on mount
  useEffect(() => {
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        if (data.gpu) {
          setGpuInfo(data.gpu);
        }
      })
      .catch((err) => {
        console.warn('Backend not yet reachable on port 8000:', err);
      });
  }, []);

  const handleGenerate = () => {
    if (!prompt.trim() || isLoading) return;

    setIsLoading(true);
    setProgressData({
      step: 1,
      total_steps: 4,
      stage: 'Connecting',
      progress: 5,
      message: 'Connecting to PolyGen AI Pipeline...'
    });

    try {
      const ws = new WebSocket(`${WS_BASE}/ws/generate`);

      ws.onopen = () => {
        ws.send(JSON.stringify({
          prompt: prompt.trim(),
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
        total_steps: 4,
        stage: 'Generating',
        progress: 50,
        message: 'Synthesizing geometry & optimizing mesh...'
      });

      const res = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: prompt.trim(),
          target_faces: targetFaces,
          detail_level: 'high'
        })
      });

      if (!res.ok) throw new Error('API request failed');
      const data: ModelMetadata = await res.json();

      setActiveModel(data);
      setProgressData({
        step: 4,
        total_steps: 4,
        stage: 'Complete',
        progress: 100,
        message: '3D Asset ready!',
        result: data
      });
    } catch (err: any) {
      alert(`Generation failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const currentGlbUrl = activeModel ? `${API_BASE}${activeModel.urls.glb}` : null;

  return (
    <div className="app-container">
      <Navbar gpuInfo={gpuInfo} />

      <main className="workspace-layout">
        <section className="viewport-area">
          <CanvasControls
            wireframe={wireframe}
            setWireframe={setWireframe}
            autoRotate={autoRotate}
            setAutoRotate={setAutoRotate}
            lightIntensity={lightIntensity}
            setLightIntensity={setLightIntensity}
          />

          <Scene3D
            modelUrl={currentGlbUrl}
            wireframe={wireframe}
            autoRotate={autoRotate}
            lightIntensity={lightIntensity}
          />

          <ProgressBar progressData={progressData} />

          <StatsCard model={activeModel} apiBase={API_BASE} />

          <PromptBar
            prompt={prompt}
            setPrompt={setPrompt}
            targetFaces={targetFaces}
            setTargetFaces={setTargetFaces}
            onGenerate={handleGenerate}
            isLoading={isLoading}
          />
        </section>
      </main>
    </div>
  );
}

export default App;
