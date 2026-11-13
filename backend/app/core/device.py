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
            info["memory_allocated_mb"] = round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2)
            info["memory_reserved_mb"] = round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2)
    except ImportError:
        pass
    return info

def get_optimal_batch_size(device_info: dict) -> int:
    if device_info.get("cuda_available") and device_info.get("vram_mb", 0) > 8000:
        return 4
    return 1
