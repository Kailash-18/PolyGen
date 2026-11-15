export interface MeshStats {
  vertices: number;
  faces: number;
  is_watertight: boolean;
  bounds: number[][] | null;
  volume: number;
  center_of_mass: number[];
}

export interface DecimationStats {
  before_faces: number;
  after_faces: number;
  decimation_ratio: number;
  reduction_percentage: string;
}

export interface ModelMetadata {
  model_id: string;
  prompt: string;
  duration_seconds: number;
  stats: MeshStats;
  decimation: DecimationStats;
  urls: {
    glb: string;
    obj: string;
  };
}

export interface ProgressUpdate {
  step: number;
  total_steps: number;
  stage: string;
  progress: number;
  message: string;
  result?: ModelMetadata;
}

export interface AssemblyPart {
  id: string;
  name: string;
  type: string;
  shape: string;
  size: number[];
  position: number[];
  rotation?: number[];
  color: string;
  material: string;
  explodeDir: number[];
  explodeDist: number;
  cornerRadius?: number;
  function?: string;
  layer?: number;
}

export interface AssemblyRelationship {
  id: string;
  from: string;
  to: string;
  type: string;
  description?: string;
}

export interface AssemblyModel {
  id: string;
  name: string;
  units: string;
  overallSize: number[];
  parts: AssemblyPart[];
  relationships: AssemblyRelationship[];
  primary_axis: string;
}

export interface TeardownStep {
  step: number;
  part_id: string;
  part_name: string;
  layer: number;
  explode_dir: number[];
  explode_dist: number;
  requires_tool: boolean;
  action: string;
}
