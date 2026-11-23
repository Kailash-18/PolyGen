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
  explodeProgress: number;
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
  explodeProgress
}: {
  url: string;
  renderMode: RenderMode;
  explodeProgress: number;
}) {
  const { scene } = useGLTF(url);
  const groupRef = useRef<THREE.Group>(null);
  const originalPositions = useRef<Map<THREE.Object3D, THREE.Vector3>>(new Map());

  scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      const mesh = child as THREE.Mesh;
      mesh.castShadow = true;
      mesh.receiveShadow = true;

      if (!originalPositions.current.has(mesh)) {
        originalPositions.current.set(mesh, mesh.position.clone());
      }

      if (renderMode === 'wireframe') {
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m) => {
            if ('wireframe' in m) (m as THREE.MeshStandardMaterial).wireframe = true;
          });
        } else if (mesh.material && 'wireframe' in mesh.material) {
          (mesh.material as THREE.MeshStandardMaterial).wireframe = true;
        }
      } else if (renderMode === 'shaded') {
        mesh.material = new THREE.MeshStandardMaterial({
          color: '#cbd5e1',
          roughness: 0.6,
          metalness: 0.1,
          wireframe: false
        });
      } else {
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m) => {
            if ('wireframe' in m) (m as THREE.MeshStandardMaterial).wireframe = false;
          });
        } else if (mesh.material && 'wireframe' in mesh.material) {
          (mesh.material as THREE.MeshStandardMaterial).wireframe = false;
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

function FallbackGeometry({ renderMode, autoRotate }: { renderMode: RenderMode; autoRotate: boolean }) {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (autoRotate && meshRef.current) {
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
  lightIntensity,
  explodeProgress
}: Scene3DProps) {
  return (
    <div className="scene-container">
      <Canvas
        shadows
        camera={{ position: [0, 2.5, 5], fov: 45 }}
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
            <LoadedModel
              url={modelUrl}
              renderMode={renderMode}
              explodeProgress={explodeProgress}
            />
          ) : (
            <FallbackGeometry renderMode={renderMode} autoRotate={autoRotate} />
          )}
        </Suspense>

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
