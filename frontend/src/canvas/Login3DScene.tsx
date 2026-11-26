import { Suspense, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Sparkles, OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// ----------------------------------------------------------------------------
// 1. Quantum Core Model
// ----------------------------------------------------------------------------
function QuantumCore() {
  const group = useRef<THREE.Group>(null);
  const innerRef = useRef<THREE.Mesh>(null);
  const ring1 = useRef<THREE.Mesh>(null);
  const ring2 = useRef<THREE.Mesh>(null);

  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.25;
    if (innerRef.current) {
      innerRef.current.rotation.y -= delta * 0.45;
      innerRef.current.rotation.z += delta * 0.3;
    }
    if (ring1.current) ring1.current.rotation.z += delta * 0.35;
    if (ring2.current) ring2.current.rotation.z -= delta * 0.28;
  });

  return (
    <group ref={group}>
      {/* Outer Wireframe Icosahedron */}
      <mesh>
        <icosahedronGeometry args={[1.5, 2]} />
        <meshStandardMaterial
          color="#38bdf8"
          roughness={0.15}
          metalness={0.85}
          wireframe
          transparent
          opacity={0.65}
        />
      </mesh>

      {/* Inner Glowing Quantum Core */}
      <mesh ref={innerRef}>
        <octahedronGeometry args={[0.95, 0]} />
        <meshStandardMaterial
          color="#0f172a"
          emissive="#6366f1"
          emissiveIntensity={1.2}
          roughness={0.2}
          metalness={0.9}
        />
      </mesh>

      {/* Dual Counter-Rotating Neon Torus Rings */}
      <mesh ref={ring1} rotation={[Math.PI / 3, 0.2, 0]}>
        <torusGeometry args={[2.0, 0.022, 16, 120]} />
        <meshBasicMaterial color="#38bdf8" />
      </mesh>
      <mesh ref={ring2} rotation={[0.7, 0.4, 0.8]}>
        <torusGeometry args={[2.25, 0.018, 16, 120]} />
        <meshBasicMaterial color="#c084fc" />
      </mesh>

      <pointLight distance={6} intensity={35} color="#38bdf8" />
      <pointLight distance={5} intensity={25} color="#a855f7" />
    </group>
  );
}

// ----------------------------------------------------------------------------
// 2. Cyber Car Model
// ----------------------------------------------------------------------------
function CyberCar() {
  const group = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.35;
  });

  return (
    <group ref={group} scale={0.95}>
      {/* Lower Chassis */}
      <mesh position={[0, 0.2, 0]}>
        <boxGeometry args={[1.4, 0.28, 2.8]} />
        <meshStandardMaterial color="#dc2626" metalness={0.85} roughness={0.2} />
      </mesh>

      {/* Front Hood */}
      <mesh position={[0, 0.28, 0.85]}>
        <boxGeometry args={[1.25, 0.16, 0.95]} />
        <meshStandardMaterial color="#b91c1c" metalness={0.9} roughness={0.15} />
      </mesh>

      {/* Cockpit Greenhouse */}
      <mesh position={[0, 0.52, -0.15]}>
        <boxGeometry args={[1.08, 0.38, 1.25]} />
        <meshStandardMaterial color="#0f172a" metalness={0.95} roughness={0.1} />
      </mesh>

      {/* Windshield Bevel */}
      <mesh position={[0, 0.48, 0.5]} rotation={[0.55, 0, 0]}>
        <boxGeometry args={[1.05, 0.28, 0.45]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Rear Spoiler */}
      <mesh position={[0, 0.65, -1.25]}>
        <boxGeometry args={[1.35, 0.06, 0.35]} />
        <meshStandardMaterial color="#0f172a" metalness={0.9} roughness={0.2} />
      </mesh>

      {/* 4 Wheels with Neon Rims */}
      {[
        [-0.75, 0.15, 0.9],
        [0.75, 0.15, 0.9],
        [-0.75, 0.15, -0.9],
        [0.75, 0.15, -0.9]
      ].map((pos, idx) => (
        <group key={idx} position={pos as [number, number, number]} rotation={[0, 0, Math.PI / 2]}>
          <mesh>
            <cylinderGeometry args={[0.3, 0.3, 0.18, 24]} />
            <meshStandardMaterial color="#1e293b" roughness={0.6} />
          </mesh>
          <mesh>
            <torusGeometry args={[0.22, 0.02, 16, 32]} />
            <meshBasicMaterial color="#38bdf8" />
          </mesh>
        </group>
      ))}

      {/* Headlights Glow */}
      <mesh position={[-0.45, 0.26, 1.4]}>
        <boxGeometry args={[0.25, 0.08, 0.05]} />
        <meshBasicMaterial color="#38bdf8" />
      </mesh>
      <mesh position={[0.45, 0.26, 1.4]}>
        <boxGeometry args={[0.25, 0.08, 0.05]} />
        <meshBasicMaterial color="#38bdf8" />
      </mesh>
    </group>
  );
}

// ----------------------------------------------------------------------------
// 3. Cyber Mech Model
// ----------------------------------------------------------------------------
function CyberMech() {
  const group = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.3;
  });

  return (
    <group ref={group} scale={0.9}>
      {/* Torso */}
      <mesh position={[0, 0.95, 0]}>
        <boxGeometry args={[1.1, 0.95, 0.8]} />
        <meshStandardMaterial color="#334155" metalness={0.8} roughness={0.25} />
      </mesh>

      {/* Glowing Chest Arc Reactor */}
      <mesh position={[0, 1.05, 0.42]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.18, 0.18, 0.06, 24]} />
        <meshBasicMaterial color="#38bdf8" />
      </mesh>

      {/* Head & Cyber Visor */}
      <mesh position={[0, 1.62, 0.05]}>
        <boxGeometry args={[0.55, 0.42, 0.48]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.2} />
      </mesh>
      <mesh position={[0, 1.62, 0.3]}>
        <boxGeometry args={[0.42, 0.12, 0.05]} />
        <meshBasicMaterial color="#00f0ff" />
      </mesh>

      {/* Shoulder Pauldrons */}
      <mesh position={[-0.85, 1.35, 0]}>
        <boxGeometry args={[0.5, 0.4, 0.6]} />
        <meshStandardMaterial color="#475569" metalness={0.85} roughness={0.2} />
      </mesh>
      <mesh position={[0.85, 1.35, 0]}>
        <boxGeometry args={[0.5, 0.4, 0.6]} />
        <meshStandardMaterial color="#475569" metalness={0.85} roughness={0.2} />
      </mesh>

      {/* Arm Weapon Pods */}
      <mesh position={[-0.92, 0.85, 0.25]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.08, 0.85, 16]} />
        <meshStandardMaterial color="#0f172a" metalness={0.9} roughness={0.3} />
      </mesh>
      <mesh position={[0.92, 0.85, 0.25]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.08, 0.85, 16]} />
        <meshStandardMaterial color="#0f172a" metalness={0.9} roughness={0.3} />
      </mesh>

      {/* Dual Articulated Legs */}
      {[-0.38, 0.38].map((dx, i) => (
        <group key={i} position={[dx, 0, 0]}>
          <mesh position={[0, 0.38, 0]}>
            <boxGeometry args={[0.26, 0.72, 0.34]} />
            <meshStandardMaterial color="#1e293b" metalness={0.85} roughness={0.3} />
          </mesh>
          <mesh position={[0, 0.04, 0.08]}>
            <boxGeometry args={[0.32, 0.14, 0.55]} />
            <meshStandardMaterial color="#0f172a" metalness={0.9} roughness={0.3} />
          </mesh>
        </group>
      ))}
    </group>
  );
}

// ----------------------------------------------------------------------------
// 4. Plasma Blade Model
// ----------------------------------------------------------------------------
function PlasmaBlade() {
  const group = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.4;
  });

  return (
    <group ref={group} scale={0.95}>
      {/* Laser Blade (Glowing) */}
      <mesh position={[0, 0.75, 0]}>
        <boxGeometry args={[0.06, 2.4, 0.24]} />
        <meshStandardMaterial
          color="#00f0ff"
          emissive="#00f0ff"
          emissiveIntensity={1.4}
          roughness={0.1}
          metalness={0.8}
        />
      </mesh>

      {/* Inner Energy Core Line */}
      <mesh position={[0, 0.75, 0]}>
        <boxGeometry args={[0.08, 2.3, 0.08]} />
        <meshBasicMaterial color="#ffffff" />
      </mesh>

      {/* Crossguard */}
      <mesh position={[0, -0.48, 0]}>
        <boxGeometry args={[0.92, 0.12, 0.22]} />
        <meshStandardMaterial color="#1e293b" metalness={0.9} roughness={0.2} />
      </mesh>

      {/* Crossguard Energy Emitters */}
      <mesh position={[-0.42, -0.48, 0]}>
        <sphereGeometry args={[0.07, 16, 16]} />
        <meshBasicMaterial color="#a855f7" />
      </mesh>
      <mesh position={[0.42, -0.48, 0]}>
        <sphereGeometry args={[0.07, 16, 16]} />
        <meshBasicMaterial color="#a855f7" />
      </mesh>

      {/* Wrapped Hilt */}
      <mesh position={[0, -0.85, 0]}>
        <cylinderGeometry args={[0.065, 0.065, 0.62, 16]} />
        <meshStandardMaterial color="#0f172a" roughness={0.8} />
      </mesh>

      {/* Pommel Orb */}
      <mesh position={[0, -1.2, 0]}>
        <sphereGeometry args={[0.11, 24, 24]} />
        <meshStandardMaterial color="#d4af37" metalness={0.9} roughness={0.1} />
      </mesh>
    </group>
  );
}

// ----------------------------------------------------------------------------
// 5. Sacred Urn / Vase Model
// ----------------------------------------------------------------------------
function SacredUrn() {
  const group = useRef<THREE.Group>(null);
  useFrame((_, delta) => {
    if (group.current) group.current.rotation.y += delta * 0.3;
  });

  return (
    <group ref={group} scale={1.1}>
      {/* Bulbous Body */}
      <mesh position={[0, 0.15, 0]}>
        <sphereGeometry args={[0.82, 32, 32]} />
        <meshStandardMaterial color="#1e293b" metalness={0.7} roughness={0.25} />
      </mesh>

      {/* Inscribed Glowing Band */}
      <mesh position={[0, 0.15, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.83, 0.025, 16, 48]} />
        <meshBasicMaterial color="#d4af37" />
      </mesh>

      {/* Tapered Neck */}
      <mesh position={[0, 0.95, 0]}>
        <cylinderGeometry args={[0.35, 0.48, 0.75, 32]} />
        <meshStandardMaterial color="#334155" metalness={0.75} roughness={0.2} />
      </mesh>

      {/* Flared Golden Rim */}
      <mesh position={[0, 1.34, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.42, 0.045, 16, 48]} />
        <meshStandardMaterial color="#d4af37" metalness={0.9} roughness={0.1} />
      </mesh>

      {/* Dual Amphora Handles */}
      <mesh position={[0.78, 0.55, 0]} rotation={[0, 0, Math.PI / 2]}>
        <torusGeometry args={[0.42, 0.04, 16, 32, Math.PI]} />
        <meshStandardMaterial color="#d4af37" metalness={0.85} roughness={0.15} />
      </mesh>
      <mesh position={[-0.78, 0.55, 0]} rotation={[0, 0, -Math.PI / 2]}>
        <torusGeometry args={[0.42, 0.04, 16, 32, Math.PI]} />
        <meshStandardMaterial color="#d4af37" metalness={0.85} roughness={0.15} />
      </mesh>

      {/* Pedestal Foot */}
      <mesh position={[0, -0.65, 0]}>
        <cylinderGeometry args={[0.48, 0.58, 0.18, 32]} />
        <meshStandardMaterial color="#d4af37" metalness={0.85} roughness={0.2} />
      </mesh>
    </group>
  );
}

// ----------------------------------------------------------------------------
// Stage Plinth Rings (Rotated Flat on Ground)
// ----------------------------------------------------------------------------
function StageRings() {
  const ringRef = useRef<THREE.Mesh>(null);
  useFrame((_, delta) => {
    if (ringRef.current) ringRef.current.rotation.z += delta * 0.12;
  });

  return (
    <group position={[0, -1.5, 0]}>
      {/* Flat Ground Disc */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.02, 0]}>
        <circleGeometry args={[2.8, 64]} />
        <meshStandardMaterial color="#080c16" roughness={0.8} metalness={0.6} />
      </mesh>

      {/* Outer Neon Cyber Ring */}
      <mesh ref={ringRef} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[2.5, 2.54, 64]} />
        <meshBasicMaterial color="#38bdf8" transparent opacity={0.65} side={THREE.DoubleSide} />
      </mesh>

      {/* Inner Accent Ring */}
      <mesh rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.7, 1.72, 64]} />
        <meshBasicMaterial color="#a855f7" transparent opacity={0.5} side={THREE.DoubleSide} />
      </mesh>

      {/* Upward Stage Glow */}
      <pointLight position={[0, 0.4, 0]} distance={4} intensity={18} color="#38bdf8" />
    </group>
  );
}

// ----------------------------------------------------------------------------
// Main Login 3D Scene Component
// ----------------------------------------------------------------------------
export function Login3DScene({ activeModel = 'core' }: { activeModel?: string }) {
  return (
    <div className="login-3d-scene-canvas-container" aria-hidden="true">
      <Canvas
        camera={{ position: [0, 0.4, 5.2], fov: 42 }}
        dpr={[1, 1.5]}
        gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      >
        <ambientLight intensity={0.85} />
        <directionalLight position={[6, 8, 5]} intensity={1.8} color="#ffffff" />
        <pointLight position={[-5, 4, 3]} intensity={25} color="#38bdf8" />
        <pointLight position={[5, -2, 2]} intensity={20} color="#a855f7" />

        <Suspense fallback={null}>
          {/* Main 3D Showcase Group - Positioned on right for cinematic split */}
          <group position={[1.4, 0.1, 0]}>
            <Float speed={1.2} rotationIntensity={0.12} floatIntensity={0.25}>
              {activeModel === 'car' && <CyberCar />}
              {activeModel === 'mech' && <CyberMech />}
              {activeModel === 'blade' && <PlasmaBlade />}
              {activeModel === 'vase' && <SacredUrn />}
              {activeModel === 'core' && <QuantumCore />}
            </Float>

            {/* Glowing Ground Plinth */}
            <StageRings />
          </group>

          {/* Drifting Cyber Sparkles */}
          <Sparkles count={120} scale={10.0} size={2.2} speed={0.25} color="#38bdf8" />
          <Sparkles count={80} scale={8.5} size={1.8} speed={0.35} color="#c084fc" />

          {/* Interactive Mouse Drag Orbit */}
          <OrbitControls
            enableZoom={false}
            enablePan={false}
            autoRotate
            autoRotateSpeed={1.0}
            maxPolarAngle={Math.PI / 2 + 0.1}
            minPolarAngle={Math.PI / 4}
          />
        </Suspense>
      </Canvas>
    </div>
  );
}

export default Login3DScene;
