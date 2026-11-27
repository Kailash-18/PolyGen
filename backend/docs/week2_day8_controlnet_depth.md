# PolyGen Week 2 Day 8 - ControlNet Depth Conditioning & Multi-View Projection Specification
**Date**: November 20, 2026
**Lead Engineer**: Sri Khyathi (Backend & 3D Generative AI)

## 1. Architectural Overview
Week 2 transitions the PolyGen pipeline from raw volumetric/neural geometry extraction to high-fidelity Physically Based Rendering (PBR) texture synthesis. 
To eliminate seam tearing and perspective distortion, we deploy a multi-camera depth-guided diffusion architecture:
1. **Multi-View Depth Rasterization**: Render depth maps from 6 canonical camera angles (Front, Back, Left, Right, Top, Bottom).
2. **ControlNet Depth Conditioning**: Condition a latent diffusion model on geometric depth buffers and user text prompts.
3. **Cross-View Projection & Blending**: Back-project generated RGB views onto 3D surfaces with normal-aware cosine angle weighting and Poisson blending.
