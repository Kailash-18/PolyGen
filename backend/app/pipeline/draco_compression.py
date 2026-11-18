"""Draco 3D Geometry Compression and Attribute Quantization Module."""
from typing import List, Tuple, Dict, Any

class DracoMeshQuantizer:
    """Quantizes floating-point vertex attributes to discrete integer grids."""
    def __init__(self, position_bits: int = 14, normal_bits: int = 10, uv_bits: int = 12):
        self.position_bits = position_bits
        self.normal_bits = normal_bits
        self.uv_bits = uv_bits

    def quantize_positions(self, vertices: List[List[float]]) -> Tuple[List[Tuple[int, int, int]], Dict[str, Any]]:
        if not vertices:
            return [], {"bounds_min": [0.0, 0.0, 0.0], "scale": 1.0, "bits": self.position_bits}
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        dx = max(max_x - min_x, 1e-6)
        dy = max(max_y - min_y, 1e-6)
        dz = max(max_z - min_z, 1e-6)
        max_extent = max(dx, dy, dz)
        max_int = (1 << self.position_bits) - 1
        scale = max_extent / max_int
        quantized = []
        for x, y, z in vertices:
            qx = int(round((x - min_x) / scale))
            qy = int(round((y - min_y) / scale))
            qz = int(round((z - min_z) / scale))
            quantized.append((max(0, min(max_int, qx)), max(0, min(max_int, qy)), max(0, min(max_int, qz))))
        return quantized, {"bounds_min": [min_x, min_y, min_z], "bounds_max": [max_x, max_y, max_z], "scale": scale, "bits": self.position_bits, "max_int": max_int}

    def dequantize_positions(self, quantized: List[Tuple[int, int, int]], metadata: Dict[str, Any]) -> List[List[float]]:
        min_x, min_y, min_z = metadata["bounds_min"]
        scale = metadata["scale"]
        return [[min_x + qx * scale, min_y + qy * scale, min_z + qz * scale] for qx, qy, qz in quantized]

    def quantize_normals(self, normals: List[List[float]]) -> Tuple[List[Tuple[int, int]], Dict[str, Any]]:
        max_int = (1 << self.normal_bits) - 1
        quantized = []
        for nx, ny, nz in normals:
            norm = abs(nx) + abs(ny) + abs(nz) or 1.0
            ox, oy = nx / norm, ny / norm
            if nz < 0:
                ox, oy = (1.0 - abs(oy)) * (1.0 if ox >= 0 else -1.0), (1.0 - abs(ox)) * (1.0 if oy >= 0 else -1.0)
            qx = int(round(((ox + 1.0) * 0.5) * max_int))
            qy = int(round(((oy + 1.0) * 0.5) * max_int))
            quantized.append((max(0, min(max_int, qx)), max(0, min(max_int, qy))))
        return quantized, {"bits": self.normal_bits, "encoding": "octahedral"}

class DracoStreamEncoder:
    """Delta encoding and run-length bitstream packer for quantized geometry buffers."""
    @staticmethod
    def delta_encode(integers: List[int]) -> List[int]:
        if not integers: return []
        deltas = [integers[0]]
        for i in range(1, len(integers)):
            deltas.append(integers[i] - integers[i - 1])
        return deltas

    @staticmethod
    def delta_decode(deltas: List[int]) -> List[int]:
        if not deltas: return []
        values = [deltas[0]]
        for i in range(1, len(deltas)):
            values.append(values[-1] + deltas[i])
        return values

    @staticmethod
    def pack_varint(value: int) -> bytes:
        zigzag = (value << 1) ^ (value >> 31)
        buf = bytearray()
        while (zigzag & ~0x7F) != 0:
            buf.append((zigzag & 0x7F) | 0x80)
            zigzag >>= 7
        buf.append(zigzag & 0x7F)
        return bytes(buf)

    @classmethod
    def compress_stream(cls, values: List[int]) -> bytes:
        deltas = cls.delta_encode(values)
        out = bytearray()
        for d in deltas:
            out.extend(cls.pack_varint(d))
        return bytes(out)

class DracoGeometryCompressor:
    """Full 3D geometry compression engine integrating attribute quantization and bit-packing."""
    def __init__(self, position_bits: int = 14, normal_bits: int = 10, uv_bits: int = 12):
        self.quantizer = DracoMeshQuantizer(position_bits, normal_bits, uv_bits)
        self.stream_encoder = DracoStreamEncoder()

    def compress(self, vertices: List[List[float]], faces: List[List[int]], normals: List[List[float]] = None) -> Dict[str, Any]:
        quantized_pos, pos_meta = self.quantizer.quantize_positions(vertices)
        flat_pos = []
        for x, y, z in quantized_pos:
            flat_pos.extend([x, y, z])
        pos_bytes = self.stream_encoder.compress_stream(flat_pos)

        flat_faces = []
        for f in faces:
            flat_faces.extend(f)
        face_bytes = self.stream_encoder.compress_stream(flat_faces)

        normal_bytes = b""
        norm_meta = None
        if normals and len(normals) == len(vertices):
            quantized_norm, norm_meta = self.quantizer.quantize_normals(normals)
            flat_norm = []
            for u, v in quantized_norm:
                flat_norm.extend([u, v])
            normal_bytes = self.stream_encoder.compress_stream(flat_norm)

        raw_pos_bytes = len(vertices) * 3 * 4
        raw_face_bytes = len(faces) * 3 * 4
        raw_norm_bytes = len(normals) * 3 * 4 if normals else 0
        raw_total = raw_pos_bytes + raw_face_bytes + raw_norm_bytes

        compressed_total = len(pos_bytes) + len(face_bytes) + len(normal_bytes)
        ratio = compressed_total / max(raw_total, 1)

        return {
            "compressed_size_bytes": compressed_total,
            "raw_size_bytes": raw_total,
            "compression_ratio": round(ratio, 4),
            "space_saving_pct": round((1.0 - ratio) * 100, 2),
            "vertex_count": len(vertices),
            "face_count": len(faces),
            "position_metadata": pos_meta,
            "normal_metadata": norm_meta,
            "payload_chunks": {
                "positions_len": len(pos_bytes),
                "faces_len": len(face_bytes),
                "normals_len": len(normal_bytes)
            }
        }
