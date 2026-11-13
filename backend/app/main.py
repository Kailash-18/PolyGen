"""
PolyGen - Generative Text-to-3D Asset Pipeline
FastAPI Backend Server Entrypoint
"""

import time
import uuid
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.core.config import settings
from app.pipeline.geometry import GeometryEngine
from app.pipeline.optimizer import MeshOptimizer
from app.pipeline.exporter import AssetExporter

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-stage Text-to-3D AI Generation & Optimization API"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated 3D files (GLB, OBJ, textures) statically
app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUTS_DIR)), name="outputs")

# Initialize Pipeline Engines
geometry_engine = GeometryEngine()
mesh_optimizer = MeshOptimizer(target_polycount=settings.DEFAULT_DECIMATION_TARGET)
asset_exporter = AssetExporter(output_root=settings.OUTPUTS_DIR)

class GenerationRequest(BaseModel):
    prompt: str = Field(..., example="A rusted medieval broadsword with a glowing blue sapphire in the hilt")
    target_faces: int = Field(default=10000, description="Target polygon count after decimation")
    detail_level: str = Field(default="high", description="Geometry detail: low, medium, high")

@app.get("/api/health")
async def health_check():
    gpu_info = {"cuda_available": False, "device_name": "CPU"}
    try:
        import torch
        if torch.cuda.is_available():
            gpu_info = {
                "cuda_available": True,
                "device_name": torch.cuda.get_device_name(0),
                "device_count": torch.cuda.device_count(),
                "memory_allocated_mb": round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2),
                "memory_reserved_mb": round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2),
            }
    except ImportError:
        pass

    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "gpu": gpu_info,
        "outputs_directory": str(settings.OUTPUTS_DIR)
    }

@app.post("/api/generate")
async def generate_asset(req: GenerationRequest):
    """Synchronous generation endpoint"""
    start_time = time.time()
    model_id = str(uuid.uuid4())[:8]

    # Stage 1: Geometry Generation
    raw_mesh = geometry_engine.generate_mesh(req.prompt, req.detail_level)

    # Stage 2: Mesh Optimization & QEM Decimation
    cleaned_mesh = mesh_optimizer.clean_and_repair(raw_mesh)
    decimated_mesh, decimation_stats = mesh_optimizer.decimate(cleaned_mesh, target_faces=req.target_faces)
    uv_mesh = mesh_optimizer.compute_uv_unwrapping(decimated_mesh)

    # Stage 3: Packaging & GLB Export
    export_info = asset_exporter.export_asset(uv_mesh, model_id)
    mesh_stats = mesh_optimizer.get_mesh_stats(uv_mesh)

    duration = round(time.time() - start_time, 2)

    # Save metadata JSON with model
    meta = {
        "model_id": model_id,
        "prompt": req.prompt,
        "duration_seconds": duration,
        "stats": mesh_stats,
        "decimation": decimation_stats,
        "urls": {
            "glb": export_info["glb_url"],
            "obj": export_info["obj_url"]
        }
    }
    meta_path = settings.OUTPUTS_DIR / model_id / "metadata.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return meta

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    """
    Real-time streaming generation endpoint that sends progress updates
    at each stage of the multi-stage 3D pipeline.
    """
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        req_json = json.loads(data)
        prompt = req_json.get("prompt", "Medieval sword")
        target_faces = int(req_json.get("target_faces", 10000))
        detail_level = req_json.get("detail_level", "high")

        model_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        # Step 1: Prompt Parsing & Geometry
        await websocket.send_json({
            "step": 1,
            "total_steps": 4,
            "stage": "Geometry Synthesis",
            "progress": 25,
            "message": f"Ingesting prompt '{prompt}' into 3D geometry engine..."
        })
        time.sleep(0.3)
        raw_mesh = geometry_engine.generate_mesh(prompt, detail_level)

        # Step 2: Mesh Optimization & QEM Decimation
        await websocket.send_json({
            "step": 2,
            "total_steps": 4,
            "stage": "Mesh Decimation & Repair",
            "progress": 55,
            "message": f"Applying Quadric Error Metrics decimation down to ~{target_faces} polygons..."
        })
        time.sleep(0.3)
        cleaned_mesh = mesh_optimizer.clean_and_repair(raw_mesh)
        decimated_mesh, decimation_stats = mesh_optimizer.decimate(cleaned_mesh, target_faces=target_faces)

        # Step 3: UV Unwrapping
        await websocket.send_json({
            "step": 3,
            "total_steps": 4,
            "stage": "UV Parameterization",
            "progress": 80,
            "message": "Computing conformal UV texture coordinates..."
        })
        time.sleep(0.3)
        uv_mesh = mesh_optimizer.compute_uv_unwrapping(decimated_mesh)

        # Step 4: GLB Packaging & Asset Export
        await websocket.send_json({
            "step": 4,
            "total_steps": 4,
            "stage": "GLB Packaging",
            "progress": 95,
            "message": "Exporting binary GLB & OBJ ready for Unreal/Unity & Three.js..."
        })
        export_info = asset_exporter.export_asset(uv_mesh, model_id)
        mesh_stats = mesh_optimizer.get_mesh_stats(uv_mesh)
        duration = round(time.time() - start_time, 2)

        result_payload = {
            "model_id": model_id,
            "prompt": prompt,
            "duration_seconds": duration,
            "stats": mesh_stats,
            "decimation": decimation_stats,
            "urls": {
                "glb": export_info["glb_url"],
                "obj": export_info["obj_url"]
            }
        }

        # Save metadata
        meta_path = settings.OUTPUTS_DIR / model_id / "metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(result_payload, f, indent=2)

        await websocket.send_json({
            "step": 4,
            "total_steps": 4,
            "stage": "Complete",
            "progress": 100,
            "message": "3D Asset successfully generated and optimized!",
            "result": result_payload
        })

    except WebSocketDisconnect:
        print("[WebSocket] Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})

@app.get("/api/models")
async def list_models():
    """List all previously generated models"""
    models = []
    if settings.OUTPUTS_DIR.exists():
        for p in settings.OUTPUTS_DIR.iterdir():
            if p.is_dir():
                meta_file = p / "metadata.json"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as f:
                            models.append(json.load(f))
                    except Exception:
                        pass
    # Sort latest first
    models.reverse()
    return {"models": models}

@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    meta_file = settings.OUTPUTS_DIR / model_id / "metadata.json"
    if not meta_file.exists():
        raise HTTPException(status_code=404, detail="Model not found")
    with open(meta_file, "r", encoding="utf-8") as f:
        return json.load(f)
