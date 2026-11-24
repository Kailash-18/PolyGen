# PolyGen Week 3 Day 12: Real-Time HDRI Environmental Staging & Tone Mapping

> **Date**: 24 November 2026  
> **Lead Engineer**: Sri Khyathi (Backend and 3D Models Track)  
> **Milestone Focus**: Image-Based Lighting (IBL), Equirectangular-to-Cubemap Projection, PMREM Radiance Convolutions & Tone Mapping  
> **Curriculum Standard**: Infotact Solutions Advanced Generative 3D AI Engineering (Vol. II)  

---

## 1. Executive Summary

Day 12 concludes the real-time lighting and viewport calibration track of PolyGen. Generating high-fidelity PBR geometry and textures is insufficient without accurate, physically grounded environmental lighting. 

This module delivers:
1. **High Dynamic Range (HDR) Environmental Staging**: Converting 360-degree equirectangular panoramic maps into high-performance cubemap radiance probes.
2. **Prefiltered Mipmapped Radiance Environment Maps (PMREM)**: Pre-integrating the GGX specular microfacet distribution across multiple perceptual roughness mip levels ($0.0$ to $1.0$).
3. **Film-Grade Tone Mapping Operators**: Implementing Academy Color Encoding System (ACES Filmic), AgX, and Reinhard dynamic range compression operators to prevent highlight clipping and color distortion.
4. **Parallax-Corrected Reflection Rig**: Enforcing localized reflection boundaries inside closed rooms and medieval vaults.
5. **Interactive Three.js Viewport Bridge**: Real-time background skybox switching, rotational alignment, and exposure calibration.

---

## 2. Mathematical Foundation: Image-Based Lighting (IBL)

### 2.1 Equirectangular-to-Cubemap Projection
Given an equirectangular texture of dimensions $W \times H$, any 3D Cartesian direction vector $v = [x, y, z]^T$ maps to spherical coordinates $(\phi, \theta)$:
$$\phi = \operatorname{atan2}(z, x), \quad \theta = \arcsin(y)$$

The normalized UV coordinate on the equirectangular map is:
$$u = \frac{\phi + \pi}{2\pi}, \quad v = \frac{\theta + \pi/2}{\pi}$$

### 2.2 ACES Filmic Tone Mapping Curve
To map high dynamic range scene luminance $x \in [0, \infty)$ to standard dynamic range display output $y \in [0, 1]$:
$$y = \frac{x(ax + b)}{x(cx + d) + e}$$
Where the Narkowicz ACES fit constants are:
$$a = 2.51, \quad b = 0.03, \quad c = 2.43, \quad d = 0.59, \quad e = 0.14$$
