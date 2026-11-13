import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    PROJECT_NAME: str = "PolyGen API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    OUTPUTS_DIR: Path = OUTPUTS_DIR
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*"
    ]
    DEFAULT_DECIMATION_TARGET: int = 10000
    ENABLE_GPU: bool = True
    MODEL_CACHE_DIR: Path = BASE_DIR / "weights"
    MOCK_3D_AI: bool = False

settings = Settings()
