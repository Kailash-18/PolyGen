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
  const modelRef = useRef<THREE.Group>(null);

  scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      const mesh = child as THREE.Mesh;
      if (Array.isArray(mesh.material)) {
        mesh.material.forEach((mat) => {
          mat.wireframe = wireframe;
        });
      } else if (mesh.material) {
        mesh.material.wireframe = wireframe;
      }
      mesh.castShadow = true;
      mesh.receiveShadow = true;
    }
  });

  return (
    <Center>
      <primitive ref={modelRef} object={scene} />
    </Center>
  );
}

export function Scene3D({ modelUrl, wireframe, autoRotate, lightIntensity }: Scene3DProps) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <Canvas
        camera={{ position: [3, 2.5, 4], fov: 45 }}
        gl={{ antialias: true, alpha: true }}
        shadows
      >
        <ambientLight intensity={0.4 * lightIntensity} />
        <directionalLight
          position={[5, 8, 5]}
          intensity={1.2 * lightIntensity}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <pointLight position={[-4, 3, -3]} intensity={0.6 * lightIntensity} color="#38bdf8" />
        <pointLight position={[4, -2, -3]} intensity={0.4 * lightIntensity} color="#a855f7" />

        <Suspense fallback={<LoadingSpinner />}>
          {modelUrl && <LoadedModel url={modelUrl} wireframe={wireframe} />}
        </Suspense>

        <Grid
          position={[0, -0.01, 0]}
          args={[20, 20]}
          cellSize={0.5}
          cellThickness={1}
          cellColor="#334155"
          sectionSize={2}
          sectionThickness={1.5}
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
