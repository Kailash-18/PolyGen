import { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Center, useGLTF, Html } from '@react-three/drei';
import * as THREE from 'three';
import type { RenderMode } from '../types';

interface Scene3DProps {
  modelUrl: string | null;
  renderMode: RenderMode;
  autoRotate: boolean;
  lightIntensity: number;
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

function LoadedModel({ url, renderMode }: { url: string; renderMode: RenderMode }) {
  const { scene } = useGLTF(url);

  scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      const mesh = child as THREE.Mesh;
      mesh.castShadow = true;
      mesh.receiveShadow = true;

      if (renderMode === 'wireframe') {
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m) => {
            if ('wireframe' in m) (m as THREE.MeshStandardMaterial).wireframe = true;
          });
        } else if (mesh.material && 'wireframe' in mesh.material) {
          (mesh.material as THREE.MeshStandardMaterial).wireframe = true;
        }
      } else if (renderMode === 'shaded') {
        // Clay inspection material
        mesh.material = new THREE.MeshStandardMaterial({
          color: '#cbd5e1',
          roughness: 0.6,
          metalness: 0.1,
          wireframe: false
        });
      } else {
        // PBR Textured Mode (original texture from GLB)
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m) => {
            if ('wireframe' in m) (m as THREE.MeshStandardMaterial).wireframe = false;
          });
        } else if (mesh.material && 'wireframe' in mesh.material) {
          (mesh.material as THREE.MeshStandardMaterial).wireframe = false;
        }
      }
    }
  });

  return (
    <Center top>
      <primitive object={scene.clone(true)} scale={1.5} />
    </Center>
  );
}

function FallbackGeometry({ renderMode }: { renderMode: RenderMode }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.4;
    }
  });

  return (
    <Center top>
      <mesh ref={meshRef} castShadow receiveShadow>
        <torusKnotGeometry args={[1, 0.35, 128, 32]} />
        <meshStandardMaterial
          color="#8b5cf6"
          roughness={0.25}
          metalness={0.8}
          wireframe={renderMode === 'wireframe'}
        />
      </mesh>
    </Center>
  );
}

export function Scene3D({
  modelUrl,
  renderMode,
  autoRotate,
  lightIntensity
}: Scene3DProps) {
  return (
    <div className="scene-container">
      <Canvas
        shadows
        camera={{ position: [0, 2, 5], fov: 45 }}
        gl={{ antialias: true, preserveDrawingBuffer: true }}
      >
        <ambientLight intensity={lightIntensity * 0.45} />
        <directionalLight
          position={[5, 8, 5]}
          intensity={lightIntensity * 1.3}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-5, 3, -5]} intensity={lightIntensity * 0.5} color="#38bdf8" />
        <pointLight position={[5, -2, 5]} intensity={lightIntensity * 0.3} color="#f43f5e" />

        <Suspense fallback={<LoadingSpinner />}>
          {modelUrl ? (
            <LoadedModel url={modelUrl} renderMode={renderMode} />
          ) : (
            <FallbackGeometry renderMode={renderMode} />
          )}
        </Suspense>

        {/* Studio Floor Grid */}
        <Grid
          renderOrder={-1}
          position={[0, -0.01, 0]}
          infiniteGrid
          cellSize={0.5}
          cellThickness={0.6}
          cellColor="#334155"
          sectionSize={2.5}
          sectionThickness={1.2}
          sectionColor="#64748b"
          fadeDistance={30}
        />

        <OrbitControls
          autoRotate={autoRotate}
          autoRotateSpeed={1.5}
          enableDamping
          dampingFactor={0.05}
          maxPolarAngle={Math.PI / 2 + 0.05}
          minDistance={1.2}
          maxDistance={15}
        />
      </Canvas>
    </div>
  );
}
