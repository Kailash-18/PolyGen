# PolyGen Week 3 Architecture: Quadric Error Metrics (QEM) Decimation & PBR Material System

> **Date**: 22 November 2026  
> **Lead Engineer**: Sri Khyathi (Backend and 3D Models Track)  
> **Target Milestone**: Week 3 Day 10 - Mesh Decimation (500k -> 10k Polygons) & Real-Time PBR Shading  
> **Curriculum Standard**: Infotact Solutions Advanced Generative 3D AI Engineering (Vol. II)  

---

## 1. Executive Overview

In Week 3 Day 10, PolyGen addresses the critical production bottleneck of AI-generated 3D meshes: excessive geometric density and unoptimized topology. Raw text-to-3D models (such as TripoSR, Shap-E, and InstantMesh) frequently produce unindexed, highly dense polygon soups containing upwards of 500,000 triangles with irregular vertex clustering and high visual noise.

This module introduces:
1. **Garland-Heckbert Quadric Error Metrics (QEM) Decimation Engine**: Efficiently simplifies 500k-polygon raw neural geometry down to a lightweight, game-ready 10k-polygon mesh while preserving geometric silhouettes, mechanical feature lines, and open topological boundaries.
2. **High-to-Low Poly Normal Map Transfer Baker**: Re-bakes the fine micro-surface normals of the 500k dense geometry onto the simplified 10k asset, ensuring zero visual fidelity loss in real-time WebGL engines.
3. **Enterprise PBR Material System**: Standardized Physically Based Rendering material parameter compiler targeting Three.js `MeshPhysicalMaterial` and Khronos glTF 2.0 with packed ORM (Occlusion-Roughness-Metallic) texture channels.

---

## 2. Mathematical Foundation: Garland-Heckbert QEM

For each triangle face $T$ in the original mesh, let its vertices be $v_0, v_1, v_2$. The supporting plane equation is defined as:
$$ax + by + cz + d = 0, \quad 	ext{where } a^2 + b^2 + c^2 = 1 	ext{ and } d = -n \cdot v_0$$

Representing the plane as homogeneous vector $p = [a, b, c, d]^T$, the fundamental error quadric $K_p \in \mathbb{R}^{4 \times 4}$ is defined as the outer product:
$$K_p = p p^T = \begin{bmatrix} a^2 & ab & ac & ad \\ ab & b^2 & bc & bd \\ ac & bc & c^2 & cd \\ ad & bd & cd & d^2 \end{bmatrix}$$

For any vertex $v$, its total geometric error quadric $Q_v$ is accumulated across all incident triangle planes:
$$Q_v = \sum_{p \in \text{planes}(v)} K_p$$

### 2.1 Edge Contraction Cost and Optimal Target Position
When contracting edge $(v_i, v_j)$ to target vertex $\bar{v}$, the combined quadric is $Q = Q_i + Q_j$.
The quadric error cost $\Delta(\bar{v})$ is quadratic:
$$\Delta(\bar{v}) = \bar{v}^T Q \bar{v} = [x, y, z, 1] Q [x, y, z, 1]^T$$

To find the position $\bar{v}$ that minimizes error, we solve $\nabla \Delta(\bar{v}) = 0$:
$$\begin{bmatrix} q_{11} & q_{12} & q_{13} & q_{14} \\ q_{12} & q_{22} & q_{23} & q_{24} \\ q_{13} & q_{23} & q_{33} & q_{34} \\ 0 & 0 & 0 & 1 \end{bmatrix} \bar{v} = \begin{bmatrix} 0 \\ 0 \\ 0 \\ 1 \end{bmatrix}$$

If the matrix is singular or poorly conditioned (condition number $> 10^4$), the solver gracefully falls back to testing candidate points: $v_i$, $v_j$, and midpoint $(v_i + v_j) / 2$, selecting the point minimizing $\Delta(\bar{v})$.

---

## 3. PBR Material Pipeline Architecture

The PBR material system unifies shading across mobile, desktop, and XR platforms:
- **Albedo / Base Color**: Rec.709 sRGB texture linearizing to linear photometric RGB.
- **Normal Map**: Tangent-space perturbation normal vector encoded as $[R, G, B] = [\frac{n_x + 1}{2}, \frac{n_y + 1}{2}, \frac{n_z + 1}{2}] \times 255$.
- **ORM Packing**:
  - Channel R: Ambient Occlusion (AO)
  - Channel G: Roughness (Perceptual linear roughness)
  - Channel B: Metallic (Conductance mask)
