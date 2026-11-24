import { Suspense, useRef, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Grid, Center, useGLTF, Html } from '@react-three/drei';
import * as THREE from 'three';
import type { RenderMode, CameraPreset, ViewportSettings } from '../types';

interface Scene3DProps {
  modelUrl: string | null;
  renderMode: RenderMode;
  autoRotate: boolean;
  lightIntensity: number;
  explodeProgress: number;
  settings: ViewportSettings;
  cameraPreset: CameraPreset;
  resetTrigger: number;
}

function LoadingSpinner() {
  return (
    <Html center>
      <div className="canvas-loader-box">
        <div className="canvas-spinner" />
        <span className="canvas-loader-text">Loading 3D Mesh & PBR Textures...</span>
      </div>
    </Html>
  );
}

function LoadedModel({
  url,
  renderMode,
  explodeProgress,
  settings
}: {
  url: string;
  renderMode: RenderMode;
  explodeProgress: number;
  settings: ViewportSettings;
}) {
  const { scene } = useGLTF(url);
  const groupRef = useRef<THREE.Group>(null);
  const originalPositions = useRef<Map<THREE.Object3D, THREE.Vector3>>(new Map());

  scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      const mesh = child as THREE.Mesh;
      mesh.castShadow = settings.showShadows;
      mesh.receiveShadow = settings.showShadows;

      if (!originalPositions.current.has(mesh)) {
        originalPositions.current.set(mesh, mesh.position.clone());
      }

      if (renderMode === 'wireframe') {
        mesh.material = new THREE.MeshBasicMaterial({
          color: settings.wireframeColor,
          wireframe: true
        });
      } else if (renderMode === 'shaded') {
        mesh.material = new THREE.MeshStandardMaterial({
          color: settings.clayColor,
          roughness: Math.max(0.05, Math.min(1.0, 0.65 * settings.roughnessMultiplier)),
          metalness: Math.max(0.0, Math.min(1.0, 0.1 * settings.metalnessMultiplier)),
          wireframe: false
        });
      } else {
        // PBR Textured Mode
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m) => {
            if ('wireframe' in m) (m as THREE.MeshStandardMaterial).wireframe = false;
            if ('roughness' in m) (m as THREE.MeshStandardMaterial).roughness = Math.min(1.0, (m as THREE.MeshStandardMaterial).roughness * settings.roughnessMultiplier);
            if ('metalness' in m) (m as THREE.MeshStandardMaterial).metalness = Math.min(1.0, (m as THREE.MeshStandardMaterial).metalness * settings.metalnessMultiplier);
          });
        } else if (mesh.material && 'wireframe' in mesh.material) {
          const std = mesh.material as THREE.MeshStandardMaterial;
          std.wireframe = false;
        }
      }

      // Kinematic Exploded View
      const orig = originalPositions.current.get(mesh);
      if (orig) {
        const dir = orig.clone().normalize();
        if (dir.lengthSq() < 0.001) dir.set(0, 1, 0);
        mesh.position.copy(orig).add(dir.multiplyScalar(explodeProgress * 1.5));
      }
    }
  });

  return (
    <Center top>
      <primitive ref={groupRef} object={scene.clone(true)} scale={1.5} />
    </Center>
  );
}

function FallbackGeometry({
  renderMode,
  autoRotate,
  settings
}: {
  renderMode: RenderMode;
  autoRotate: boolean;
  settings: ViewportSettings;
}) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (autoRotate && meshRef.current) {
      meshRef.current.rotation.y += delta * 0.4;
    }
  });

  let geomColor = '#8b5cf6';
  let roughnessVal = 0.25 * settings.roughnessMultiplier;
  let metalnessVal = 0.8 * settings.metalnessMultiplier;
  let isWire = renderMode === 'wireframe';

  if (renderMode === 'shaded') {
    geomColor = settings.clayColor;
    roughnessVal = 0.65;
    metalnessVal = 0.1;
  } else if (renderMode === 'wireframe') {
    geomColor = settings.wireframeColor;
  }

  return (
    <Center top>
      <mesh ref={meshRef} castShadow={settings.showShadows} receiveShadow={settings.showShadows}>
        <torusKnotGeometry args={[1, 0.35, 128, 32]} />
        <meshStandardMaterial
          color={geomColor}
          roughness={Math.max(0.05, Math.min(1.0, roughnessVal))}
          metalness={Math.max(0.0, Math.min(1.0, metalnessVal))}
          wireframe={isWire}
        />
      </mesh>
    </Center>
  );
}

function CameraRig({
  preset,
  resetTrigger,
  autoRotate
}: {
  preset: CameraPreset;
  resetTrigger: number;
  autoRotate: boolean;
}) {
  const { camera } = useThree();
  const controlsRef = useRef<any>(null);

  useEffect(() => {
    if (controlsRef.current) {
      if (preset === 'front') {
        camera.position.set(0, 0, 4.8);
      } else if (preset === 'top') {
        camera.position.set(0, 5.5, 0.001);
      } else if (preset === 'side') {
        camera.position.set(4.8, 0, 0);
      } else if (preset === 'isometric') {
        camera.position.set(3.5, 3.5, 3.5);
      } else {
        camera.position.set(0, 2.5, 5);
      }
      camera.lookAt(0, 0, 0);
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
    }
  }, [preset, resetTrigger, camera]);

  return (
    <OrbitControls
      ref={controlsRef}
      autoRotate={autoRotate}
      autoRotateSpeed={1.5}
      enableDamping
      dampingFactor={0.05}
      maxPolarAngle={Math.PI / 2 + 0.05}
      minDistance={1.0}
      maxDistance={15}
    />
  );
}

export function Scene3D({
  modelUrl,
  renderMode,
  autoRotate,
  lightIntensity,
  explodeProgress,
  settings,
  cameraPreset,
  resetTrigger
}: Scene3DProps) {
  return (
    <div className="scene-container">
      <Canvas
        shadows={settings.showShadows}
        camera={{ position: [0, 2.5, 5], fov: 45 }}
        gl={{ antialias: true, preserveDrawingBuffer: true }}
      >
        <ambientLight intensity={lightIntensity * 0.45} />
        <directionalLight
          position={[5, 8, 5]}
          intensity={lightIntensity * 1.3}
          castShadow={settings.showShadows}
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-5, 3, -5]} intensity={lightIntensity * 0.5} color="#38bdf8" />
        <pointLight position={[5, -2, 5]} intensity={lightIntensity * 0.3} color="#f43f5e" />

        <Suspense fallback={<LoadingSpinner />}>
          {modelUrl ? (
            <LoadedModel
              url={modelUrl}
              renderMode={renderMode}
              explodeProgress={explodeProgress}
              settings={settings}
            />
          ) : (
            <FallbackGeometry
              renderMode={renderMode}
              autoRotate={autoRotate}
              settings={settings}
            />
          )}
        </Suspense>

        {settings.showGrid && (
          <Grid
            renderOrder={-1}
            position={[0, -0.01, 0]}
            infiniteGrid
            cellSize={0.6}
            cellThickness={0.5}
            cellColor="#1e2230"
            sectionSize={3.0}
            sectionThickness={0.9}
            sectionColor="#2d3548"
            fadeDistance={24}
          />
        )}

        <CameraRig
          preset={cameraPreset}
          resetTrigger={resetTrigger}
          autoRotate={autoRotate}
        />
      </Canvas>
    </div>
  );
}
