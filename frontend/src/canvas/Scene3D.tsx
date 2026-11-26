import { Suspense, useRef, useEffect, useMemo, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Grid, Center, useGLTF, Html, ContactShadows } from '@react-three/drei';
import * as THREE from 'three';
import type { RenderMode, CameraPreset, ViewportSettings } from '../types';
// @ts-ignore
import { soundFx } from './audio3d.js';

interface Scene3DProps {
  modelUrl: string | null;
  renderMode: RenderMode;
  autoRotate: boolean;
  lightIntensity: number;
  explodeProgress: number;
  settings: ViewportSettings;
  cameraPreset: CameraPreset;
  resetTrigger: number;
  showKinematics?: boolean;
}

function LoadingSpinner() {
  return (
    <Html center>
      <div className="canvas-loader-box">
        <div className="scan-line-sweep" />
        <div className="canvas-spinner-ring" />
        <div className="canvas-loader-text-group">
          <span className="canvas-loader-title">Synthesizing 3D Geometry</span>
          <span className="canvas-loader-sub">Streaming vertex buffers & PBR materials...</span>
        </div>
      </div>
    </Html>
  );
}

// 3D Floating Leader Callout Badge with SVG leader pointer
function PartLeaderBadge({
  position,
  label,
  subLabel,
  color = '#38bdf8'
}: {
  position: [number, number, number];
  label: string;
  subLabel?: string;
  color?: string;
}) {
  return (
    <Html position={position} center distanceFactor={8} zIndexRange={[100, 0]}>
      <div className="callout-leader-card pointer-events-none select-none">
        <div className="callout-dot" style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }} />
        <div className="callout-box">
          <span className="callout-title" style={{ color }}>{label}</span>
          {subLabel && <span className="callout-sub">{subLabel}</span>}
        </div>
      </div>
    </Html>
  );
}

// Dynamic Floating Cyber Particles in 3D Space
function CyberParticles({ count = 45 }: { count?: number }) {
  const points = useMemo(() => {
    const coords = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      coords[i * 3] = (Math.random() - 0.5) * 8.0;
      coords[i * 3 + 1] = Math.random() * 4.5 + 0.2;
      coords[i * 3 + 2] = (Math.random() - 0.5) * 8.0;
    }
    return coords;
  }, [count]);

  const geomRef = useRef<THREE.BufferGeometry>(null);

  useFrame((_, delta) => {
    if (!geomRef.current) return;
    const pos = geomRef.current.attributes.position;
    for (let i = 0; i < count; i++) {
      let y = pos.getY(i) + delta * 0.15;
      if (y > 4.8) y = 0.2;
      pos.setY(i, y);
    }
    pos.needsUpdate = true;
  });

  return (
    <points>
      <bufferGeometry ref={geomRef}>
        <bufferAttribute
          attach="attributes-position"
          args={[points, 3]}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.065}
        color="#38bdf8"
        transparent
        opacity={0.45}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

// Center-of-Mass & Kinematics Coordinate Axes (RGB = XYZ)
function KinematicsAxes({ position = [0, 1.0, 0] }: { position?: [number, number, number] }) {
  return (
    <group position={position}>
      {/* Center of Mass Indicator Sphere */}
      <mesh>
        <sphereGeometry args={[0.07, 16, 16]} />
        <meshBasicMaterial color="#f59e0b" wireframe />
      </mesh>
      {/* X Axis Arrow (Red) */}
      <mesh position={[0.4, 0, 0]} rotation={[0, 0, -Math.PI / 2]}>
        <cylinderGeometry args={[0.015, 0.015, 0.8, 8]} />
        <meshBasicMaterial color="#ef4444" />
      </mesh>
      {/* Y Axis Arrow (Green) */}
      <mesh position={[0, 0.4, 0]}>
        <cylinderGeometry args={[0.015, 0.015, 0.8, 8]} />
        <meshBasicMaterial color="#10b981" />
      </mesh>
      {/* Z Axis Arrow (Blue) */}
      <mesh position={[0, 0, 0.4]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.015, 0.015, 0.8, 8]} />
        <meshBasicMaterial color="#3b82f6" />
      </mesh>
    </group>
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
  const clonedScene = useMemo(() => scene.clone(true), [scene]);
  const originalPositions = useRef<Map<THREE.Object3D, THREE.Vector3>>(new Map());
  const [meshNodes, setMeshNodes] = useState<{ mesh: THREE.Mesh; origPos: THREE.Vector3 }[]>([]);

  // Collect meshes & apply materials, vertex colors, and shadow settings
  useEffect(() => {
    const nodes: { mesh: THREE.Mesh; origPos: THREE.Vector3 }[] = [];

    clonedScene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = settings.showShadows;
        mesh.receiveShadow = settings.showShadows;

        if (!originalPositions.current.has(mesh)) {
          originalPositions.current.set(mesh, mesh.position.clone());
        }

        const orig = originalPositions.current.get(mesh) || mesh.position.clone();
        nodes.push({ mesh, origPos: orig });

        const hasVertexColors = !!(mesh.geometry && mesh.geometry.attributes && mesh.geometry.attributes.color);

        if (renderMode === 'wireframe') {
          mesh.material = new THREE.MeshBasicMaterial({
            color: settings.wireframeColor || '#00f0ff',
            wireframe: true
          });
        } else if (renderMode === 'shaded') {
          mesh.material = new THREE.MeshStandardMaterial({
            color: settings.clayColor || '#e2e8f0',
            roughness: Math.max(0.1, Math.min(1.0, 0.55 * settings.roughnessMultiplier)),
            metalness: Math.max(0.0, Math.min(1.0, 0.1 * settings.metalnessMultiplier)),
            wireframe: false
          });
        } else {
          // PBR Mode - ensure vertex colors and specular highlights are active
          if (Array.isArray(mesh.material)) {
            mesh.material = mesh.material.map((m) => {
              const std = (m as THREE.MeshStandardMaterial).clone();
              std.wireframe = false;
              if (hasVertexColors) std.vertexColors = true;
              std.roughness = Math.max(0.15, Math.min(0.75, 0.35 * settings.roughnessMultiplier));
              std.metalness = Math.max(0.1, Math.min(0.65, 0.35 * settings.metalnessMultiplier));
              std.needsUpdate = true;
              return std;
            });
          } else if (mesh.material) {
            const std = (mesh.material as THREE.MeshStandardMaterial).clone();
            std.wireframe = false;
            if (hasVertexColors) std.vertexColors = true;
            std.roughness = Math.max(0.15, Math.min(0.75, 0.35 * settings.roughnessMultiplier));
            std.metalness = Math.max(0.1, Math.min(0.65, 0.35 * settings.metalnessMultiplier));
            std.needsUpdate = true;
            mesh.material = std;
          }
        }
      }
    });

    setMeshNodes(nodes);
  }, [clonedScene, renderMode, settings]);

  // Handle Exploded View Kinematics with sound effects
  useEffect(() => {
    soundFx.updateExplodeAudio(explodeProgress);

    clonedScene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        const orig = originalPositions.current.get(mesh);
        if (orig) {
          const dir = orig.clone().normalize();
          if (dir.lengthSq() < 0.001) dir.set(0, 1, 0);
          mesh.position.copy(orig).add(dir.multiplyScalar(explodeProgress * 1.7));
        }
      }
    });
  }, [clonedScene, explodeProgress]);

  // Gentle subtle breathing float animation when not exploded
  const groupRef = useRef<THREE.Group>(null);
  useFrame(({ clock }) => {
    if (groupRef.current && explodeProgress <= 0.02) {
      const t = clock.getElapsedTime();
      groupRef.current.position.y = Math.sin(t * 1.4) * 0.04;
    } else if (groupRef.current) {
      groupRef.current.position.y = 0;
    }
  });

  // Measure exact bounds and auto-normalize scale so model is NEVER clipped or oversized
  const { normalizedScale, offsetX, verticalOffset, offsetZ } = useMemo(() => {
    const box = new THREE.Box3().setFromObject(clonedScene);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const maxDim = Math.max(size.x, size.y, size.z);
    const targetDim = 1.9; // Optimal hero scale in 3D viewport
    const scale = maxDim > 0.01 ? targetDim / maxDim : 1.0;
    return {
      normalizedScale: scale,
      offsetX: -center.x * scale,
      verticalOffset: -box.min.y * scale,
      offsetZ: -center.z * scale
    };
  }, [clonedScene]);

  return (
    <group position={[offsetX, verticalOffset, offsetZ]}>
      <group ref={groupRef}>
        <primitive object={clonedScene} scale={normalizedScale} />

        {/* 3D Floating Part Leaders when Exploded */}
        {explodeProgress > 0.15 &&
          meshNodes.slice(0, 4).map((node, idx) => {
            const worldPos = new THREE.Vector3();
            node.mesh.getWorldPosition(worldPos);
            const titles = ['Core Structure', 'Sub-Assembly', 'Actuator Flange', 'Kinematic Link'];
            const subs = ['Titanium grade', 'PBR mapped', 'Watertight', 'Dynamic offset'];
            return (
              <PartLeaderBadge
                key={idx}
                position={[worldPos.x, worldPos.y + 0.35, worldPos.z]}
                label={titles[idx % titles.length]}
                subLabel={subs[idx % subs.length]}
                color={idx === 0 ? '#38bdf8' : idx === 1 ? '#a855f7' : idx === 2 ? '#34d399' : '#fbbf24'}
              />
            );
          })}
      </group>
    </group>
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

  let geomColor = '#6366f1';
  let roughnessVal = 0.3 * settings.roughnessMultiplier;
  let metalnessVal = 0.4 * settings.metalnessMultiplier;
  const isWire = renderMode === 'wireframe';

  if (renderMode === 'shaded') {
    geomColor = settings.clayColor || '#e2e8f0';
    roughnessVal = 0.55;
    metalnessVal = 0.1;
  } else if (renderMode === 'wireframe') {
    geomColor = settings.wireframeColor || '#00f0ff';
  }

  return (
    <Center top>
      <mesh ref={meshRef} castShadow={settings.showShadows} receiveShadow={settings.showShadows}>
        <torusKnotGeometry args={[0.9, 0.32, 128, 32]} />
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
        camera.position.set(0, 1.1, 4.4);
      } else if (preset === 'top') {
        camera.position.set(0, 5.2, 0.001);
      } else if (preset === 'side') {
        camera.position.set(4.4, 1.1, 0);
      } else if (preset === 'isometric') {
        camera.position.set(3.2, 2.8, 3.2);
      } else {
        camera.position.set(0, 1.2, 4.4);
      }
      camera.lookAt(0, 0.95, 0);
      controlsRef.current.target.set(0, 0.95, 0);
      controlsRef.current.update();
    }
  }, [preset, resetTrigger, camera]);

  return (
    <OrbitControls
      ref={controlsRef}
      autoRotate={autoRotate}
      autoRotateSpeed={1.8}
      enableDamping
      dampingFactor={0.06}
      maxPolarAngle={Math.PI / 2 + 0.08}
      minDistance={1.0}
      maxDistance={20}
    />
  );
}

// Circular Studio Stage Plinth with glowing outer bevel & rotating tick marks
function StudioPedestal() {
  const ticksRef = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (ticksRef.current) ticksRef.current.rotation.z += delta * 0.06;
  });

  return (
    <group position={[0, -0.015, 0]}>
      {/* Dark metallic circular stage */}
      <mesh receiveShadow position={[0, -0.05, 0]}>
        <cylinderGeometry args={[2.85, 2.95, 0.1, 64]} />
        <meshStandardMaterial
          color="#131724"
          roughness={0.65}
          metalness={0.25}
        />
      </mesh>
      {/* Outer neon bevel ring (flat on the floor in XZ) */}
      <mesh position={[0, 0.006, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[2.8, 2.88, 64]} />
        <meshBasicMaterial
          color="#6366f1"
          transparent
          opacity={0.45}
          side={THREE.DoubleSide}
        />
      </mesh>
      {/* Slowly revolving concentric tick ring (flat on the floor in XZ) */}
      <mesh ref={ticksRef} position={[0, 0.007, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[2.4, 2.45, 32]} />
        <meshBasicMaterial
          color="#38bdf8"
          transparent
          opacity={0.25}
          wireframe
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
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
  resetTrigger,
  showKinematics = false
}: Scene3DProps) {
  return (
    <div className="scene-container">
      {/* Cybernetic HUD Reticle Overlay */}
      <div className="canvas-hud-overlay pointer-events-none">
        <i className="br tl" />
        <i className="br tr" />
        <i className="br bl" />
        <i className="br brr" />
        <div className="hud-radar-ring" />
      </div>

      <Canvas
        shadows={settings.showShadows}
        camera={{ position: [0, 1.2, 4.4], fov: 38 }}
        gl={{
          antialias: true,
          preserveDrawingBuffer: true,
          toneMapping: THREE.ACESFilmicToneMapping,
          toneMappingExposure: 1.35
        }}
      >
        {/* Balanced Ambient & Hemisphere Lighting */}
        <ambientLight intensity={lightIntensity * 1.2} />
        <hemisphereLight args={['#ffffff', '#1e293b', lightIntensity * 1.1]} />

        {/* Studio Key Light (warm white with soft shadow) */}
        <directionalLight
          position={[5, 9, 6]}
          intensity={lightIntensity * 2.2}
          castShadow={settings.showShadows}
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
          shadow-bias={-0.0001}
        />

        {/* Fill Light (cool sky blue for clear silhouette) */}
        <directionalLight
          position={[-6, 6, -4]}
          intensity={lightIntensity * 1.4}
          color="#93c5fd"
        />

        {/* Rim / Back Light (electric violet/cyan accent for edge definition) */}
        <directionalLight
          position={[0, 6, -7]}
          intensity={lightIntensity * 1.6}
          color="#a855f7"
        />

        {/* Under-Bounce Uplight */}
        <pointLight
          position={[0, -2, 0]}
          intensity={lightIntensity * 0.7}
          color="#38bdf8"
        />

        {/* 3D Model with Suspense */}
        <Suspense fallback={<LoadingSpinner />}>
          {modelUrl ? (
            <LoadedModel
              key={modelUrl}
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

        {/* Center of Mass & Kinematics Axes */}
        {showKinematics && <KinematicsAxes position={[0, 0.9, 0]} />}

        {/* Ambient Floating Dust / Cyber Particles */}
        <CyberParticles count={45} />

        {/* Studio Pedestal & Contact Soft Shadows */}
        <StudioPedestal />
        <ContactShadows
          position={[0, 0, 0]}
          opacity={0.7}
          scale={7.5}
          blur={1.8}
          far={3.5}
        />

        {/* Studio Grid Floor */}
        {settings.showGrid && (
          <Grid
            renderOrder={-1}
            position={[0, -0.01, 0]}
            infiniteGrid
            cellSize={0.5}
            cellThickness={0.6}
            cellColor="#1e2638"
            sectionSize={2.5}
            sectionThickness={1.0}
            sectionColor="#334155"
            fadeDistance={30}
          />
        )}

        <CameraRig
          preset={cameraPreset}
          resetTrigger={resetTrigger}
          autoRotate={autoRotate}
        />
      </Canvas>

      {/* Cybernetic HUD Frame Overlay */}
      <div className="canvas-hud-overlay pointer-events-none select-none">
        {/* Corner Reticles */}
        <div className="hud-corner tl" />
        <div className="hud-corner tr" />
        <div className="hud-corner bl" />
        <div className="hud-corner br" />

        {/* Top Left Telemetry Tag */}
        <div className="hud-telemetry-tag">
          <span className="hud-beacon-dot" />
          <span className="hud-tag-title">SYS.3D // KINEMATICS ACTIVE</span>
          <span className="hud-tag-divider">|</span>
          <span className="hud-tag-sub">60 FPS · PBR SHADER · ACES FILMIC</span>
        </div>

        {/* Center Subtle Targeting Reticle */}
        <div className="hud-crosshair-center">
          <div className="hud-reticle-circle" />
          <div className="hud-cross-line x" />
          <div className="hud-cross-line y" />
        </div>

        {/* Subtle Laser Scanline Sweep */}
        <div className="hud-scanline-laser" />
      </div>
    </div>
  );
}

export default Scene3D;
