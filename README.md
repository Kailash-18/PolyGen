# PolyGen: Generative Text-to-3D Asset Pipeline

> **Autonomous multi-stage pipeline converting descriptive text prompts into optimized, PBR-textured, game-ready 3D assets (`.glb` / `.obj`) with real-time WebGL canvas inspection.**

[![Status](https://img.shields.io/badge/Status-Active_Development-blue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11-brightgreen.svg)](#)
[![React](https://img.shields.io/badge/Frontend-React%20%7C%20Three.js-61DAFB.svg)](#)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20PyTorch-009688.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](#)

---

## 📌 Problem Statement

Creating 3D assets for video games, XR, metaverse environments, and visual simulations is an intensely manual and expensive process:
1. **Time Sink**: A 3D artist spends hours in Blender/Maya manually blocking geometry, sculpting high-poly details, retopologizing, UV unwrapping, and hand-painting PBR textures.
2. **Cost Barrier**: Independent studios and solo developers cannot afford the weeks or months required to populate 3D worlds with hundreds of bespoke props and environment models.
3. **Existing AI Limitations**: Standard 2D AI image generators only produce flat images. Existing NeRF/Splatting optimization methods take 20–40 minutes per object and generate heavy, non-game-ready meshes with millions of unoptimized polygons.

---

## 🚀 The Solution: PolyGen

**PolyGen** solves this by chaining state-of-the-art generative 3D models with classical computational geometry into an autonomous, 4-stage pipeline:

```
                          ┌────────────────────────┐
                          │   Natural Language     │
                          │     Text Prompt        │
                          └───────────┬────────────┘
                                      │
                                      ▼
                      ┌────────────────────────────────┐
                      │   Stage 1: Geometry Generation │
                      │      (TripoSR / Shap-E)        │
                      │  • Feed-forward reconstruction │
                      │  • Initial 3D mesh (.obj)      │
                      └───────────────┬────────────────┘
                                      │
                                      ▼
                      ┌────────────────────────────────┐
                      │   Stage 2: Mesh Optimization   │
                      │       (Trimesh & Open3D)       │
                      │  • QEM Decimation (500k -> 10k)│
                      │  • Automatic UV Parameterization│
                      └───────────────┬────────────────┘
                                      │
                                      ▼
                      ┌────────────────────────────────┐
                      │   Stage 3: Texture Synthesis   │
                      │ (Stable Diffusion + ControlNet)│
                      │  • Depth & Normal guidance     │
                      │  • PBR Maps (Albedo, Roughness)│
                      └───────────────┬────────────────┘
                                      │
                                      ▼
                      ┌────────────────────────────────┐
                      │    Stage 4: Packaging & Web    │
                      │  • Standard .glb / .gltf export│
                      │  • Real-time Three.js viewer   │
                      │  • Ready for Unreal / Unity    │
                      └────────────────────────────────┘
```

---

## 🛠️ Technology Stack & Justifications

| Component | Technology | Why We Are Using It |
| :--- | :--- | :--- |
| **3D Geometry AI** | **TripoSR / Shap-E (PyTorch)** | Feed-forward Large Reconstruction Models (LRMs) generate raw 3D meshes in **under 5 seconds on GPU**, avoiding the 30-minute training times of traditional NeRF optimization. |
| **Mesh Optimization** | **Trimesh & Open3D** | Raw AI geometry is dense and noisy (~500k polygons). Trimesh performs **Quadric Error Metrics (QEM) decimation** to reduce polycount to ~10k and calculates conformal **UV maps** required for texturing. |
| **Texture Synthesis** | **Stable Diffusion + ControlNet** | Produces high-resolution textures aligned with the geometry's depth and surface normals, preventing seams and texture distortion. |
| **Backend API** | **FastAPI + WebSockets** | Asynchronous Python server that manages GPU memory, coordinates multi-stage pipeline tasks, and streams progress updates to the frontend. |
| **3D Web Studio** | **React + Three.js + React-Three-Fiber** | Provides an in-browser 3D canvas with OrbitControls, PBR material rendering (Roughness, Metalness, Normal maps), and HDRI environment lighting. |
| **Target Output** | **GLTF / GLB** | The open standard "JPEG of 3D". Encapsulates geometry, materials, and textures into a single file ready for immediate drag-and-drop into Unreal Engine 5, Unity, or Blender. |

---

## 📁 Repository Structure

```
PolyGen/
├── backend/                  # FastAPI & Python AI Pipeline
│   ├── app/
│   │   ├── api/              # API routes & WebSocket endpoints
│   │   ├── core/             # Configuration & GPU device handlers
│   │   ├── pipeline/         # Multi-stage generation logic
│   │   │   ├── geometry.py   # TripoSR / Shap-E mesh inference
│   │   │   ├── optimizer.py  # Trimesh QEM decimation & UV unwrapping
│   │   │   ├── texture.py    # ControlNet & Stable Diffusion texturing
│   │   │   └── exporter.py   # GLB / GLTF binary packager
│   │   └── main.py           # Application entrypoint
│   └── requirements.txt      # Python dependencies (PyTorch, Trimesh, FastAPI)
│
├── frontend/                 # Interactive 3D Web Studio
│   ├── src/
│   │   ├── components/       # UI Controls, Prompt Input, Asset History
│   │   ├── canvas/           # Three.js / React-Three-Fiber Viewport
│   │   │   ├── ModelViewer.tsx   # OrbitControls, Mesh loader, PBR renderer
│   │   │   ├── Lighting.tsx      # HDRI studio lighting & directional lights
│   │   │   └── Wireframe.tsx     # Topology inspection overlay
│   │   ├── hooks/            # WebSocket generation hooks
│   │   ├── App.tsx           # Main application view
│   │   └── main.tsx          # React root
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                     # Architecture diagrams, specifications, notes
├── .gitignore                # Git ignore rules for node_modules, weights, and caches
└── README.md                 # Project documentation
```

---

## 🗓️ 4-Week Milestone Roadmap

### **Week 1: Foundations & Geometry**
- **3D Canvas**: Scaffold the React application using Vite, Tailwind CSS, and `@react-three/fiber` to load and render 3D meshes with basic lighting and OrbitControls.
- **Mesh Generation Backend**: Scaffold the FastAPI backend and configure GPU-accelerated mesh generation (TripoSR / Shap-E) to produce raw `.obj` files from text prompts.

### **Week 2: UV Mapping & Texture Synthesis**
- **Mesh Processing**: Write Python automation with `trimesh` to calculate automatic UV coordinates and unwrap the generated mesh.
- **Texture Generation**: Integrate Stable Diffusion + depth/normal ControlNet to synthesize textures matching the prompt.
- **Mid-Project Audit**: Validate that recognizable 3D structures (e.g., weapons, furniture, props) are generated with mapped textures.

### **Week 3: Decimation & PBR Material System**
- **QEM Decimation**: Implement Quadric Error Metrics decimation to reduce 500k-polygon raw AI meshes down to game-ready ~10k polygons.
- **PBR Materials**: Upgrade the Three.js viewport to render full Physically Based Rendering maps (Albedo, Normal maps, Roughness, Metalness).

### **Week 4: Export Pipeline & Studio Polish**
- **Export Pipeline**: Convert meshes and textures into standard `.glb` and `.gltf` formats for seamless integration into Unreal Engine and Unity.
- **Studio Polish**: Add HDRI environment maps for realistic lighting, wireframe topology toggle, and asset download controls.

---

## ⚙️ Quick Start

### Prerequisites
- **Node.js** >= 18 (Node v24 recommended)
- **Python** 3.10 or 3.11 with an NVIDIA CUDA-capable GPU (RTX series recommended)
- **Git**

### 1. Clone the Repository
```bash
git clone https://github.com/Kailash-18/PolyGen.git
cd PolyGen
```

### 2. Backend Setup
```bash
cd backend
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.
