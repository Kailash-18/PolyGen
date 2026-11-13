import os

def detect_compute_device(preferred: str = "auto") -> dict:
    info = {"device": "cpu", "cuda_available": False, "device_name": "CPU", "vram_mb": 0}
    if preferred == "cpu":
        return info
    try:
        import torch
        if torch.cuda.is_available():
            info["device"] = "cuda:0"
            info["cuda_available"] = True
            info["device_name"] = torch.cuda.get_device_name(0)
            info["vram_mb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024 * 1024), 2)
    except ImportError:
        pass
    return info
