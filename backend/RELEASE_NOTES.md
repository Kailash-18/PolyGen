# PolyGen Release Notes - Milestone Week 1-4

## Release v1.2.0 - Week 4 Final Review: Game Engine Export Pipeline & Studio Staging
**Author**: Sri Khyathi Ambadipudi (`ambadipudisrikhyathi@gmail.com`)  
**Date**: 17 November 2026  
**Status**: Production Ready & Verified (83/83 Tests Passing - 100%)

---

### Highlights & Key Features Delivered (Day 5 - 17 Nov 2026)

1. **Multi-LOD Generation Engine (`app.pipeline.lod`)**:
   - Automated cascaded LOD0, LOD1, LOD2, and LOD3 mesh simplification using Quadric Error Metrics (QEM).
   - Normalized one-sided Hausdorff geometric error auditing ensuring sub-pixel silhouette retention.
   - Screen size transition thresholds calibrated to Unreal Engine 5 and Unity LODGroup standards.

2. **Epic Games Unreal Engine 5 Package Exporter (`app.pipeline.game_engine_exporter`)**:
   - Packages ready-to-import ZIP bundles with strict `SM_<Asset>` static mesh conventions.
   - Decoupled PBR maps (`T_<Asset>_D`, `T_<Asset>_N`, `T_<Asset>_R`, `T_<Asset>_M`).
   - Automated `UnrealAssetManifest.json` generation with Nanite triangle threshold recommendations.

3. **Unity 2022/6000 LTS URP & HDRP Prefab Exporter**:
   - Generates Unity prefab archives with `.prefab` component serializations.
   - Industry-standard channel packing: Red = Metallic, Alpha = Smoothness ($255 - \text{Roughness}$).
   - Pre-configured `LODGroup` screen percentage thresholds and MeshCollider specifications.

4. **Physics Collision Hull Decomposition (`app.pipeline.collision_hull`)**:
   - Computes simplified convex hulls ($\le 64$ vertices) exported as `UCX_<Asset>_01.obj`.
   - Generates minimal Oriented Bounding Boxes (OBB) aligned with principal component axes.
   - Computes Axis-Aligned Bounding Boxes (AABB) and bounding capsule proxies.

5. **Physically Calibrated PBR Material Presets (`app.pipeline.pbr_presets`)**:
   - 6 production material presets: `Cyberpunk Neon`, `Weathered Rust`, `Sci-Fi Matte`, `Anodized Titanium`, `Obsidian Glass`, and `24k Gold Leaf`.
   - Real-time texture map baking and live Three.js shader parameter modulation.

6. **Studio HDRI Environment Lighting (`app.pipeline.hdri_staging`)**:
   - 4 photometric lighting rigs calibrated by correlated color temperature: `Neutral Industrial (5600K)`, `Neo-Tokyo Cyberpunk (8500K)`, `Golden Sunset (3200K)`, and `Void Deep Space (6500K)`.
   - Three.js WebGL exposure and shadow casting integration.

7. **Interactive Game Engine Export Modal & Viewer Staging (`viewer/export-lab.js`)**:
   - One-click client export modal supporting engine selection, LOD toggles, and instant ZIP downloading.
   - Dynamic PBR preset switching pills with live WebGL material updating.

8. **Comprehensive 83-Test Automated Suite**:
   - 100% test pass rate across geometry, optimization, textures, kinematics, BOM, box eval, LODs, collisions, PBR presets, HDRI staging, and game engine exporters.

---

## Release v1.1.0 - Backend & 3D Models Deliverables
**Author**: Sri Khyathi Ambadipudi (`ambadipudisrikhyathi@gmail.com`)  
**Date**: 15 November 2026  
**Status**: Production Ready & Verified (100% Tests Passing)

---

### Highlights & Key Features Delivered

1. **Procedural Geometry Engine**:
   - Synthesizes watertight 3D polygonal meshes for mechanical and organic assets.
   - Built-in parametric generators for Cybernetic Broadsword, Aegis Shield, Crystal Clusters, Grecian Ceramic Vases, Ergonomic Task Chairs, and Robotic Arms.

2. **Mesh Topology Optimizer**:
   - Quadric Error Metrics (QEM) decimation reducing 100k+ polygons down to target polycounts with silhouette preservation.
   - Conformal spherical and cylindrical UV mapping algorithms.
   - Automated non-manifold repair and hole filling.

3. **PBR Texture Map Synthesis**:
   - 4-channel Physically Based Rendering maps: Albedo, Normal, Roughness, and Metalness.
   - Tangent-space normal vector perturbation from heightmaps.

4. **3D Assembly Kinematics Engine**:
   - Multi-part component hierarchy with parent-child relationships (`powers`, `feeds`, `controls`, `mounts`, `drives`, `transmits`, `supports`).
   - Unit-normalized directional explosion vectors (`explode_dir`) and radial distance multipliers (`explode_dist`).
   - Monotonic clearance solver guaranteeing zero-collision component separation.

5. **Advanced Interactive 3D Animation Suite**:
   - Exploded-view continuous scrubber slider (0% to 100%).
   - Cinematic Auto-Play Assembly Loop with sinusoidal easing and showroom apex pause.
   - Sequential Teardown Wave Ripple animation cascading outward through assembly layers.
   - Custom GLSL Holographic Blueprint shader (`holo3d.js`) with drifting scanlines and Fresnel glow.
   - Dynamic Laser X-Ray scanner sweep (`xray3d.js`) revealing internal electronic wiring.
   - Guided interactive 3D inspection tour (`tour.js`) and assembly particle FX (`build-fx.js`).

6. **Full REST & WebSocket API**:
   - FastAPI backend with CORS middleware, streaming progress telemetry, and model catalog persistence.
