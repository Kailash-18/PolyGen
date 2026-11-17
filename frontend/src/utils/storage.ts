/**
 * Safe Browser Storage Manager with Fallback
 * Part of PolyGen 3D Generative Pipeline - Frontend
 */

export class SafeStorage {
  private static memoryFallback: Map<string, string> = new Map();

  static getItem<T>(key: string, defaultValue: T): T {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const item = window.localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
      }
    } catch (e) {
      console.warn(`localStorage read error for key "${key}":`, e);
    }
    const memItem = this.memoryFallback.get(key);
    return memItem ? JSON.parse(memItem) : defaultValue;
  }

  static setItem<T>(key: string, value: T): boolean {
    try {
      const serialized = JSON.stringify(value);
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem(key, serialized);
        return true;
      }
      this.memoryFallback.set(key, serialized);
      return true;
    } catch (e) {
      console.warn(`localStorage write error for key "${key}":`, e);
      return false;
    }
  }

  static removeItem(key: string): void {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.removeItem(key);
      }
    } catch (e) {
      console.warn(`localStorage remove error for key "${key}":`, e);
    }
    this.memoryFallback.delete(key);
  }
}
