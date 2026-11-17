/**
 * Color and PBR Texture Linearization Utilities
 * Part of PolyGen 3D Generative Pipeline - Frontend
 */

/**
 * Convert hex color string to normalized RGB array [0.0 - 1.0]
 */
export function hexToRgbNormalized(hex: string): [number, number, number] {
  const cleanHex = hex.replace('#', '');
  const bigint = parseInt(cleanHex, 16);
  const r = ((bigint >> 16) & 255) / 255;
  const g = ((bigint >> 8) & 255) / 255;
  const b = (bigint & 255) / 255;
  return [r, g, b];
}

/**
 * Convert sRGB gamma-corrected component to Linear RGB space for PBR shaders
 */
export function sRGBToLinear(c: number): number {
  return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
}

/**
 * Convert Linear RGB component to sRGB space for display
 */
export function linearToSRGB(c: number): number {
  return c <= 0.0031308 ? c * 12.92 : 1.055 * Math.pow(c, 1.0 / 2.4) - 0.055;
}

/**
 * Calculate relative luminance using Rec. 709 coefficients
 */
export function getRelativeLuminance(r: number, g: number, b: number): number {
  return 0.2126 * sRGBToLinear(r) + 0.7152 * sRGBToLinear(g) + 0.0722 * sRGBToLinear(b);
}
