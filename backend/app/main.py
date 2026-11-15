"""
PolyGen - Generative Text-to-3D Asset Pipeline
FastAPI Backend Server Entrypoint with 3D Assembly Kinematics
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
from app.core.device import detect_compute_device
from app.pipeline.geometry import GeometryEngine
from app.pipeline.optimizer import MeshOptimizer
from app.pipeline.texture import TextureEngine
from app.pipeline.exporter import AssetExporter
from app.pipeline.assembly import AssemblyEngine, AssemblyModel, ExplosionPose

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-stage Text-to-3D AI Generation & 3D Assembly Kinematics API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

geometry_engine = GeometryEngine()
mesh_optimizer = MeshOptimizer(target_polycount=settings.DEFAULT_DECIMATION_TARGET)
texture_engine = TextureEngine(resolution=512)
asset_exporter = AssetExporter(output_root=settings.OUTPUTS_DIR)

app.mount("/outputs", StaticFiles(directory=str(settings.OUTPUTS_DIR)), name="outputs")

VIEWER_DIR = Path(__file__).resolve().parent.parent.parent / "viewer"
if VIEWER_DIR.exists():
    app.mount("/viewer", StaticFiles(directory=str(VIEWER_DIR), html=True), name="viewer")

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "samples"

class GenerationRequest(BaseModel):
    prompt: str = Field(..., json_schema_extra={"example": "A rusted medieval broadsword with a glowing blue sapphire in the hilt"})
    target_faces: int = Field(default=10000, description="Target polygon count after decimation")
    detail_level: str = Field(default="high", description="Geometry detail: low, medium, high")

class ExplodeRequest(BaseModel):
    progress: float = Field(default=0.75, ge=0.0, le=1.0, description="Exploded view trajectory factor 0.0 to 1.0")

@app.get("/api/physical/samples")
async def list_physical_samples():
    items = []
    if SAMPLES_DIR.exists():
        for f in sorted(SAMPLES_DIR.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
                items.append({
                    "id": f.stem,
                    "title": d.get("title", f.stem.replace("-", " ").title())
                })
            except Exception:
                continue
    return {
        "samples": items,
        "note": "Reference 3D models and verified mechanical assemblies."
    }

@app.get("/api/physical/samples/{sample_id}")
async def get_physical_sample(sample_id: str):
    clean_id = sample_id.replace("-", "").replace("_", "")
    if not clean_id.isalnum():
        raise HTTPException(400, "Invalid sample ID")
    f = SAMPLES_DIR / f"{sample_id}.json"
    if not f.exists():
        raise HTTPException(404, "Sample not found")
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(500, f"Error reading sample: {e}")

@app.get("/api/health")
async def health_check():
    gpu_info = detect_compute_device()
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "gpu": gpu_info,
        "outputs_directory": str(settings.OUTPUTS_DIR)
    }

@app.post("/api/generate")
async def generate_asset(req: GenerationRequest):
    start_time = time.time()
    model_id = str(uuid.uuid4())[:8]

    raw_mesh = geometry_engine.generate_mesh(req.prompt, req.detail_level)
    cleaned_mesh = mesh_optimizer.clean_and_repair(raw_mesh)
    decimated_mesh, decimation_stats = mesh_optimizer.decimate(cleaned_mesh, target_faces=req.target_faces)
    uv_mesh = mesh_optimizer.compute_uv_unwrapping(decimated_mesh)

    pbr_maps = texture_engine.synthesize_pbr_maps(req.prompt, uv_mesh)
    textured_mesh = texture_engine.apply_textures_to_mesh(uv_mesh, pbr_maps)

    export_info = asset_exporter.export_asset(textured_mesh, model_id, pbr_maps=pbr_maps)
    mesh_stats = mesh_optimizer.get_mesh_stats(textured_mesh)
    duration = round(time.time() - start_time, 2)

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
    asset_exporter.save_metadata(model_id, meta)
    return meta

@app.get("/api/models/{model_id}/assembly", response_model=AssemblyModel)
async def get_model_assembly(model_id: str):
    return AssemblyEngine.get_assembly(model_id)

@app.post("/api/models/{model_id}/assembly/explode")
async def calculate_assembly_explode(model_id: str, req: ExplodeRequest):
    assembly = AssemblyEngine.get_assembly(model_id)
    poses = AssemblyEngine.calculate_explosion_pose(assembly, req.progress)
    return {
        "model_id": model_id,
        "progress": req.progress,
        "poses": [p.model_dump() for p in poses]
    }

@app.get("/api/assemblies")
async def list_sample_assemblies():
    return {
        "assemblies": [
            AssemblyEngine.create_drone_assembly().model_dump(by_alias=True),
            AssemblyEngine.create_broadsword_assembly().model_dump(by_alias=True),
            AssemblyEngine.create_shield_assembly().model_dump(by_alias=True),
            AssemblyEngine.create_chair_assembly().model_dump(by_alias=True),
            AssemblyEngine.create_robotic_arm_assembly().model_dump(by_alias=True)
        ]
    }

@app.websocket("/ws/generate")
async def websocket_generate(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        req_json = json.loads(data)
        prompt = req_json.get("prompt", "Medieval sword")
        target_faces = int(req_json.get("target_faces", 10000))
        detail_level = req_json.get("detail_level", "high")

        model_id = str(uuid.uuid4())[:8]
        start_time = time.time()

        await websocket.send_json({
            "step": 1,
            "total_steps": 4,
            "stage": "Geometry Synthesis",
            "progress": 25,
            "message": f"Ingesting prompt '{prompt}' into 3D geometry engine..."
        })
        raw_mesh = geometry_engine.generate_mesh(prompt, detail_level)

        await websocket.send_json({
            "step": 2,
            "total_steps": 4,
            "stage": "Mesh Decimation & Repair",
            "progress": 55,
            "message": f"Applying Quadric Error Metrics decimation down to ~{target_faces} polygons..."
        })
        cleaned_mesh = mesh_optimizer.clean_and_repair(raw_mesh)
        decimated_mesh, decimation_stats = mesh_optimizer.decimate(cleaned_mesh, target_faces=target_faces)

        await websocket.send_json({
            "step": 3,
            "total_steps": 4,
            "stage": "UV Parameterization & Texturing",
            "progress": 80,
            "message": "Computing conformal UV coordinates and synthesizing PBR materials..."
        })
        uv_mesh = mesh_optimizer.compute_uv_unwrapping(decimated_mesh)
        pbr_maps = texture_engine.synthesize_pbr_maps(prompt, uv_mesh)
        textured_mesh = texture_engine.apply_textures_to_mesh(uv_mesh, pbr_maps)

        await websocket.send_json({
            "step": 4,
            "total_steps": 4,
            "stage": "GLB Packaging",
            "progress": 95,
            "message": "Exporting binary GLB & OBJ ready for Unreal/Unity & Three.js..."
        })
        export_info = asset_exporter.export_asset(textured_mesh, model_id, pbr_maps=pbr_maps)
        mesh_stats = mesh_optimizer.get_mesh_stats(textured_mesh)
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
        asset_exporter.save_metadata(model_id, result_payload)

        await websocket.send_json({
            "step": 4,
            "total_steps": 4,
            "stage": "Complete",
            "progress": 100,
            "message": "3D Asset successfully generated and optimized!",
            "result": result_payload
        })
    except WebSocketDisconnect:
        pass
    except Exception as e:
        await websocket.send_json({"error": str(e)})

@app.get("/api/models")
async def list_models():
    models = []
    if settings.OUTPUTS_DIR.exists():
        for p in settings.OUTPUTS_DIR.iterdir():
            if p.is_dir():
                meta_file = p / "metadata.json"
                if meta_file.exists():
                    try:
                        with open(meta_file, "r", encoding="utf-8") as meta_f:
                            models.append(json.load(meta_f))
                    except Exception:
                        pass
    models.reverse()
    return {"models": models}

@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    meta_file = settings.OUTPUTS_DIR / model_id / "metadata.json"
    if not meta_file.exists():
        raise HTTPException(status_code=404, detail="Model not found")
    with open(meta_file, "r", encoding="utf-8") as meta_f:
        return json.load(meta_f)
