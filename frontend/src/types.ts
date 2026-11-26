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
  created_at?: string;
  stats: MeshStats;
  decimation: DecimationStats;
  textures?: {
    albedo?: string;
    normal?: string;
    roughness?: string;
  };
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

export interface UserProfile {
  name: string;
  displayName?: string;
  email: string;
  role: string;
  plan: string;
  avatar: string;
}

export type ThemeMode = 'dark' | 'light';
export type ActiveTab = 'studio' | 'explore' | 'library' | 'audit';
export type RenderMode = 'pbr' | 'shaded' | 'wireframe';
export type CameraPreset = 'default' | 'front' | 'top' | 'side' | 'isometric';

export interface ViewportSettings {
  showGrid: boolean;
  showShadows: boolean;
  clayColor: string;
  wireframeColor: string;
  roughnessMultiplier: number;
  metalnessMultiplier: number;
}
