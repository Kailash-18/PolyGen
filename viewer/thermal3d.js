// PolyGen Thermal3D Engine - FLIR Thermal Stress & Heat Dissipation Shader
// Visualizes thermodynamic heat dissipation across mechanical components in real time.
import * as THREE from "three";

const THERMAL_VERT = /* glsl */`
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  varying vec3 vWorldPosition;
  void main() {
    vNormal = normalize(normalMatrix * normal);
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    vViewPosition = -mvPosition.xyz;
    vWorldPosition = (modelMatrix * vec4(position, 1.0)).xyz;
    gl_Position = projectionMatrix * mvPosition;
  }
`;

const THERMAL_FRAG = /* glsl */`
  uniform float uTime;
  uniform float uHeatBaseline;
  uniform float uHeatIntensity;
  uniform vec3 uHeatCenter;
  varying vec3 vNormal;
  varying vec3 vViewPosition;
  varying vec3 vWorldPosition;

  // Scientific FLIR Ironbow / Infrared thermal colormap
  vec3 thermalColor(float t) {
    t = clamp(t, 0.0, 1.0);
    vec3 c0 = vec3(0.05, 0.05, 0.25); // 20°C Ambient Deep Blue
    vec3 c1 = vec3(0.15, 0.45, 0.85); // 35°C Cyan
    vec3 c2 = vec3(0.95, 0.65, 0.10); // 55°C Amber Warm
    vec3 c3 = vec3(0.95, 0.15, 0.05); // 75°C Radiant Red
    vec3 c4 = vec3(1.00, 0.98, 0.90); // 95°C White Hot

    if (t < 0.25) return mix(c0, c1, t / 0.25);
    if (t < 0.50) return mix(c1, c2, (t - 0.25) / 0.25);
    if (t < 0.75) return mix(c2, c3, (t - 0.50) / 0.25);
    return mix(c3, c4, (t - 0.75) / 0.25);
  }

  void main() {
    vec3 N = normalize(vNormal);
    vec3 V = normalize(vViewPosition);
    float fresnel = pow(1.0 - abs(dot(N, V)), 2.5);

    // Distance from active thermal core
    float d = length(vWorldPosition - uHeatCenter);
    float pulse = 0.5 + 0.5 * sin(uTime * 3.0 - d * 2.5);
    float temp = clamp(uHeatBaseline + (uHeatIntensity * 0.75) / (1.0 + d * 0.8) + pulse * 0.08, 0.0, 1.0);

    vec3 col = thermalColor(temp);
    // Emissive thermal rim glow
    col += vec3(0.8, 0.2, 0.1) * fresnel * 0.6;

    gl_FragColor = vec4(col, 0.92);
  }
`;

export function installThermal(View) {
  const P = View.prototype;

  P.thermalFor = function (p) {
    if (p.thermalMat) return p.thermalMat;
    const g = p.mesh.geometry;
    const u = {
      uTime: { value: 0 },
      uHeatBaseline: { value: 0.15 },
      uHeatIntensity: { value: 0.85 },
      uHeatCenter: { value: new THREE.Vector3(0, 0, 0) }
    };

    // Components that generate extreme heat get elevated baseline temperatures
    const name = (p.id || "").toLowerCase();
    if (name.includes("cpu") || name.includes("processor") || name.includes("gpu") || name.includes("chip")) {
      u.uHeatBaseline.value = 0.78;
    } else if (name.includes("battery") || name.includes("power") || name.includes("motor")) {
      u.uHeatBaseline.value = 0.55;
    } else if (name.includes("copper") || name.includes("heat") || name.includes("pipe") || name.includes("board")) {
      u.uHeatBaseline.value = 0.38;
    }

    const mat = new THREE.ShaderMaterial({
      uniforms: u,
      vertexShader: THERMAL_VERT,
      fragmentShader: THERMAL_FRAG,
      transparent: true,
      side: THREE.DoubleSide
    });

    p.thermalMat = mat;
    p.thermalUniforms = u;
    return mat;
  };

  P.setThermalMode = function (active) {
    this.thermalActive = active;
    for (const p of this.parts) {
      if (active) {
        if (!p.origMat) p.origMat = p.mat;
        p.mesh.material = this.thermalFor(p);
      } else {
        if (p.origMat) p.mesh.material = p.origMat;
      }
    }
    this.poke?.();
  };

  const origRender = P.render;
  P.render = function () {
    if (this.thermalActive) {
      const now = performance.now() / 1000;
      for (const p of this.parts) {
        if (p.thermalUniforms) {
          p.thermalUniforms.uTime.value = now;
        }
      }
    }
    if (origRender) origRender.call(this);
  };
}
