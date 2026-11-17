# PolyGen Game Engine Export Pipeline & LOD Specification

> **Technical Architecture Guide for Week 4 / Final Review Deliverables**  
> **Author**: Sri Khyathi Ambadipudi (`ambadipudisrikhyathi@gmail.com`)  
> **Date**: 17 November 2026  
> **Release Version**: v1.2.0

---

## 1. Overview & Problem Context

Spatial generative AI models (such as TripoSR and Shap-E) produce continuous neural radiance field reconstructions that can be extracted as polygonal meshes. However, raw AI-generated meshes are non-game-ready:
1. **Excessive Topology**: Vertex counts frequently exceed 100,000 to 500,000 unindexed polygons with irregular triangle topology and non-manifold boundaries.
2. **Missing Physics Colliders**: Game engines cannot use complex visual meshes for real-time physics collisions without causing CPU simulation stalls.
3. **Lack of LOD Groups**: Real-time rendering engines require cascaded Levels of Detail (LODs) to maintain steady 60-120 FPS across open worlds and crowded scenes.
4. **Channel Mismatch**: Different engines require disparate texture channel packings (e.g. Unity combines Metallic into Red and Smoothness into Alpha, whereas Unreal Engine separates Roughness and Metallic).

**PolyGen v1.2.0** provides automated, production-grade export pipelines targeting **Epic Games Unreal Engine 5** and **Unity URP / HDRP**.

---

## 2. Multi-LOD Generation Architecture

The Multi-LOD engine (`backend/app/pipeline/lod.py`) takes master geometry and computes a 4-tier cascaded LOD hierarchy using Quadric Error Metrics (QEM) edge collapse decimation:

| LOD Level | Polygon Budget | Target Ratio | Screen Size Threshold | Target Use-Case |
| :--- | :--- | :--- | :--- | :--- |
| **LOD0** | 100% of Master | 1.00 | $\ge 0.70$ (Hero / Closeup) | Full visual fidelity, cinematic cutscenes, showroom inspect |
| **LOD1** | 50% Reduction | 0.50 | $\ge 0.40$ (Mid-Range) | Third-person gameplay camera, nearby interactable props |
| **LOD2** | 25% Reduction | 0.25 | $\ge 0.15$ (Far View) | Medium distance environment placement, multiplayer crowd |
| **LOD3** | 10% Reduction | 0.10 | $\ge 0.05$ (Background Proxy) | Horizon silhouettes, background vistas, low-poly shadows |

### Hausdorff Distance Metric
For each generated LOD mesh $M_i$, the geometric error relative to the master mesh $M_0$ is audited using normalized one-sided Hausdorff distance:

$$d_H(M_0, M_i) = \frac{\max_{p \in V_0} \min_{q \in S_i} \|p - q\|}{\text{diag}(\text{AABB}(M_0))}$$

PolyGen enforces $d_H(M_0, M_3) < 0.15$, guaranteeing silhouette fidelity even at 90% polygon reduction.

---

## 3. Physics Collision Hull Decomposition

The physics collision engine (`backend/app/pipeline/collision_hull.py`) synthesizes low-poly collision proxies:

### 1. Convex Hull (`UCX_<AssetName>_01`)
- Computed using quickhull bounding algorithm, simplified to $\le 64$ vertices.
- Perfectly suited for rigid bodies, physics pickups, and projectile impact testing.

### 2. Oriented Bounding Box (`UBX_<AssetName>_01`)
- Oriented along principal component axes (PCA) of vertex distribution.
- Lowest-overhead box collision check for rectilinear furniture and mechanical assemblies.

### 3. Bounding Capsule (`UCP_<AssetName>_01`)
- Dominant vertical axis aligned with spherical hemispherical caps.
- Optimized for character locomotion blockers and cylindrical props.

---

## 4. Unreal Engine 5 Packaging Pipeline

Unreal Engine 5 requires strict naming conventions and asset layouts. PolyGen exports a self-contained ZIP containing:

```
Unreal_CyberKatana/
├── SM_CyberKatana.glb               # LOD0 Master Static Mesh
├── SM_CyberKatana_LOD1.glb          # 50% Decimated LOD1
├── SM_CyberKatana_LOD2.glb          # 25% Decimated LOD2
├── SM_CyberKatana_LOD3.glb          # 10% Decimated LOD3
├── UCX_CyberKatana_01.obj           # Physics Convex Hull Collider
├── T_CyberKatana_D.png              # Diffuse / Base Color Map
├── T_CyberKatana_N.png              # Tangent Space Normal Map
├── T_CyberKatana_R.png              # Grayscale Roughness Map
├── T_CyberKatana_M.png              # Grayscale Metallic Map
└── UnrealAssetManifest.json         # UStaticMesh & Nanite Config
```

### Unreal Engine Asset Manifest Schema
```json
{
  "unreal_engine_version": "5.4+",
  "asset_class": "UStaticMesh",
  "asset_name": "SM_CyberKatana",
  "nanite_settings": {
    "enabled_recommended": true,
    "keep_percent_triangles": 1.0,
    "trim_relative_error": 0.04
  },
  "collision_settings": {
    "custom_collision": true,
    "collision_complexity": "UseSimpleAsComplex"
  }
}
```

---

## 5. Unity URP & HDRP Prefab Pipeline

Unity uses combined texture channels to reduce texture sampler calls during fragment shader evaluation.

### Metallic-Smoothness Channel Packing
PolyGen packs Metallic and Smoothness into a single 4-channel RGBA texture:
- **Red (R)**: Metallic value ($0\dots 255$)
- **Green (G)**: $0$ (Unused)
- **Blue (B)**: $0$ (Unused)
- **Alpha (A)**: Smoothness ($255 - \text{Roughness}$)

```
Unity_AegisShield/
├── AegisShield.glb                  # Master Mesh
├── AegisShield_LOD1.glb             # LOD1 Mesh
├── AegisShield_LOD2.glb             # LOD2 Mesh
├── AegisShield_LOD3.glb             # LOD3 Mesh
├── AegisShield_Albedo.png           # Base Color
├── AegisShield_Normal.png           # Tangent Normal Map
├── AegisShield_MetallicSmoothness.png # Packed (R=Metallic, A=Smoothness)
└── UnityPackageManifest.json        # Prefab & LODGroup Specification
```

---

## 6. Photometric Studio HDRI Lighting Rigs

The HDRI engine (`backend/app/pipeline/hdri_staging.py`) provides 4 studio environments calibrated by correlated color temperature (CCT):

1. **Neutral Industrial Studio (5600K)**: Balanced 3-point key/fill/back light with soft floor shadow for technical evaluation.
2. **Neo-Tokyo Cyberpunk Rig (8500K)**: Complementary electric cyan ($#00\text{E}5\text{FF}$) and hot magenta ($#\text{FF}007\text{F}$) rim lighting.
3. **Golden Hour Sunset (3200K)**: Warm low-angle tungsten sun with cool atmospheric sky bounce ($#6\text{C}8\text{CD}5$).
4. **Void Deep Space (6500K)**: High-contrast single stellar beam with deep indigo nebula fill ($#0\text{A}1838$).

---

## 7. Verification & Test Suite

The test suite covers 83 automated unit tests with 100% pass rate:
- `test_lod.py`: Validates decimation ratios, monotonicity, and Hausdorff error bounds.
- `test_collision_hull.py`: Audits convex hull volume, OBB extents, and UCX export structure.
- `test_pbr_presets.py`: Tests 6 physically calibrated material presets and map baking.
- `test_hdri_staging.py`: Verifies CCT lighting rigs and directional light vectors.
- `test_gltf_packager.py`: Validates binary GLB 4-byte alignment and chunk headers.
- `test_game_engine_exporter.py`: Tests Unreal and Unity ZIP creation and manifest integrity.
- `test_api.py`: End-to-end FastAPI endpoint integration tests.
