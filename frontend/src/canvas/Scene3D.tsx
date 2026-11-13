import { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Grid, Center, useGLTF, Html } from '@react-three/drei';
import * as THREE from 'three';

interface Scene3DProps {
  modelUrl: string | null;
  wireframe: boolean;
  autoRotate: boolean;
  lightIntensity: number;
}

function LoadingSpinner() {
  return (
    <Html center>
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: '12px',
        color: '#fff',
        fontFamily: 'sans-serif',
        background: 'rgba(15, 23, 42, 0.85)',
        padding: '16px 24px',
        borderRadius: '12px',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(8px)'
      }}>
        <div style={{
          width: '32px',
          height: '32px',
          border: '3px solid rgba(168, 85, 247, 0.2)',
          borderTopColor: '#a855f7',
          borderRadius: '50%',
          animation: 'spin 0.8s linear infinite'
        }} />
        <span style={{ fontSize: '14px', fontWeight: 500 }}>Loading 3D Mesh...</span>
      </div>
    </Html>
  );
}

function LoadedModel({ url, wireframe }: { url: string; wireframe: boolean }) {
  const { scene } = useGLTF(url);

  // Apply wireframe and ensure materials handle lighting
  scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      const mesh = child as THREE.Mesh;
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      if (Array.isArray(mesh.material)) {
        mesh.material.forEach((m) => {
          if ('wireframe' in m) {
            (m as THREE.MeshStandardMaterial).wireframe = wireframe;
          }
        });
      } else if (mesh.material && 'wireframe' in mesh.material) {
        (mesh.material as THREE.MeshStandardMaterial).wireframe = wireframe;
      }
    }
  });

  return (
    <Center top>
      <primitive object={scene.clone(true)} scale={1.5} />
    </Center>
  );
}

function FallbackGeometry({ wireframe }: { wireframe: boolean }) {
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
          wireframe={wireframe}
        />
      </mesh>
    </Center>
  );
}

export function Scene3D({
  modelUrl,
  wireframe,
  autoRotate,
  lightIntensity
}: Scene3DProps) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative', background: 'radial-gradient(circle at 50% 50%, #1e1e2f 0%, #0d0e15 100%)' }}>
      <Canvas
        shadows
        camera={{ position: [0, 2, 5], fov: 45 }}
        gl={{ antialias: true, preserveDrawingBuffer: true }}
      >
        <ambientLight intensity={lightIntensity * 0.4} />
        <directionalLight
          position={[5, 8, 5]}
          intensity={lightIntensity * 1.2}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-5, 3, -5]} intensity={lightIntensity * 0.5} color="#38bdf8" />
        <pointLight position={[5, -2, 5]} intensity={lightIntensity * 0.3} color="#f43f5e" />

        <Suspense fallback={<LoadingSpinner />}>
          {modelUrl ? (
            <LoadedModel url={modelUrl} wireframe={wireframe} />
          ) : (
            <FallbackGeometry wireframe={wireframe} />
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
