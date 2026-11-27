# PolyGen Week 3 Day 11: Advanced PBR Shading Engine & Khronos Extensions

> **Date**: 23 November 2026  
> **Lead Engineer**: Sri Khyathi (Backend and 3D Models Track)  
> **Milestone Focus**: Advanced Physically Based Rendering, Dual-Layer Clearcoat, Multi-UV Sets & Khronos KHR Extension Suite  
> **Curriculum Standard**: Infotact Solutions Advanced Generative 3D AI Engineering (Vol. II)  

---

## 1. Executive Summary

Day 11 advances PolyGen's material rendering capabilities from baseline metallic-roughness shading to an enterprise-grade physically based rendering (PBR) engine. Modern real-time 3D environments (such as Three.js WebGL and Unreal Engine / Unity via glTF 2.0) require optical models capable of simulating complex materials:
- **Lacquered and Coated Surfaces**: Medieval polished steel armor, lacquered wooden sword hilts, and vehicle automotive finishes requiring secondary clearcoat reflection layers.
- **Translucent and Crystalline Materials**: Glowing sapphires, gems, stained glass, and organic surfaces requiring Index of Refraction (IOR) Fresnel calculation, volume absorption (Beer-Lambert attenuation), and transmission.
- **Multi-UV Coordinate Sets**: UV0 for high-frequency tiled albedo/normal maps and UV1 for non-overlapping lightmaps and baked ambient occlusion.
- **Khronos Extension Serialization**: Standardized metadata export conforming to `KHR_materials_clearcoat`, `KHR_materials_ior`, `KHR_materials_transmission`, `KHR_materials_volume`, and `KHR_materials_emissive_strength`.

---

## 2. Microfacet Shading Mathematics

### 2.1 Cook-Torrance Specular BRDF
The specular bidirectional reflectance distribution function (BRDF) is formulated as:
$$f_r(l, v) = \frac{D(h) F(v, h) G(l, v, h)}{4 (n \cdot l) (n \cdot v)}$$

Where:
- $D(h)$ is the Trowbridge-Reitz GGX normal distribution function.
- $F(v, h)$ is the Fresnel-Schlick reflection factor evaluated from base reflectance $F_0$.
- $G(l, v, h)$ is the Smith geometric shadowing-masking term with GGX visibility.

### 2.2 Generalized Fresnel from Index of Refraction (IOR)
For dielectric materials with index of refraction $n_{\text{mat}}$ in medium $n_{\text{med}}$ (air $\approx 1.0$), normal incidence reflectance $F_0$ is derived directly:
$$F_0 = \left( \frac{n_{\text{mat}} - n_{\text{med}}}{n_{\text{mat}} + n_{\text{med}}} \right)^2$$

For instance:
- Air-to-Water ($n=1.33$): $F_0 = 0.02$
- Air-to-Glass ($n=1.50$): $F_0 = 0.04$
- Air-to-Sapphire ($n=1.77$): $F_0 = 0.077$
- Air-to-Diamond ($n=2.42$): $F_0 = 0.172$

### 2.3 Dual-Layer Clearcoat Attenuation
A clearcoat layer forms a secondary dielectric interface above the substrate. The composite specular reflection combines the clearcoat reflectance $R_c$ and underlying base reflectance $R_b$:
$$R_{\text{total}} = R_c + (1 - R_c)^2 R_b$$
