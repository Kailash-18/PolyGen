/**
 * 3D Geometry and Vector Mathematics Utilities
 * Part of PolyGen 3D Generative Pipeline - Frontend
 */

export interface Vector3D {
  x: number;
  y: number;
  z: number;
}

export interface BoundingBox3D {
  min: Vector3D;
  max: Vector3D;
  center: Vector3D;
  extents: Vector3D;
}

/**
 * Calculate bounding box extents and geometric center from vertex coordinate array
 */
export function computeBoundingBox(vertices: number[][]): BoundingBox3D {
  if (!vertices || vertices.length === 0) {
    const zero = { x: 0, y: 0, z: 0 };
    return { min: zero, max: zero, center: zero, extents: zero };
  }

  let minX = Infinity, minY = Infinity, minZ = Infinity;
  let maxX = -Infinity, maxY = -Infinity, maxZ = -Infinity;

  for (const v of vertices) {
    if (v[0] < minX) minX = v[0];
    if (v[0] > maxX) maxX = v[0];
    if (v[1] < minY) minY = v[1];
    if (v[1] > maxY) maxY = v[1];
    if (v[2] < minZ) minZ = v[2];
    if (v[2] > maxZ) maxZ = v[2];
  }

  const min = { x: minX, y: minY, z: minZ };
  const max = { x: maxX, y: maxY, z: maxZ };
  const center = {
    x: (minX + maxX) / 2,
    y: (minY + maxY) / 2,
    z: (minZ + maxZ) / 2
  };
  const extents = {
    x: maxX - minX,
    y: maxY - minY,
    z: maxZ - minZ
  };

  return { min, max, center, extents };
}

/**
 * Euclidean distance between two 3D spatial points
 */
export function distance3D(a: Vector3D, b: Vector3D): number {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  const dz = a.z - b.z;
  return Math.sqrt(dx * dx + dy * dy + dz * dz);
}
