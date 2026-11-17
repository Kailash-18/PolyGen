/**
 * 3D Asset Snapshot and Mesh Export Utilities
 * Author: Kailash-18
 */

export function generateExportFilename(modelId: string, ext: 'glb' | 'obj' | 'png'): string {
  const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return `polygen_${modelId || 'asset'}_${timestamp}.${ext}`;
}

export function triggerDownload(url: string, filename: string): void {
  if (typeof document === 'undefined') return;
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
