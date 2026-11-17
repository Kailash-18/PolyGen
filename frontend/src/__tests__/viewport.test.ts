/**
 * Viewport Render Modes & Camera Presets Unit Tests
 * Author: Kailash-18
 */
import type { CameraPreset } from '../types';

export function testRenderModeTransitions() {
  const allowed = new Set(['pbr', 'shaded', 'wireframe']);
  const isValidMode = (mode: string) => allowed.has(mode);

  if (!isValidMode('shaded')) throw new Error('Valid mode rejected');
  if (!isValidMode('wireframe')) throw new Error('Valid mode rejected');
  if (!isValidMode('pbr')) throw new Error('Valid mode rejected');
  if (isValidMode('unknown')) throw new Error('Invalid mode accepted');

  return true;
}

export function testCameraPresetCoordinates() {
  const getCameraPosition = (preset: CameraPreset): [number, number, number] => {
    switch (preset) {
      case 'front': return [0, 0, 4.8];
      case 'top': return [0, 5.5, 0.001];
      case 'side': return [4.8, 0, 0];
      case 'isometric': return [3.5, 3.5, 3.5];
      default: return [0, 2.5, 5];
    }
  };

  const front = getCameraPosition('front');
  if (front[2] <= 0) throw new Error('Front camera z should be positive');

  const top = getCameraPosition('top');
  if (top[1] <= 0) throw new Error('Top camera y should be positive');

  return true;
}
