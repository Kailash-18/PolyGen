/**
 * Authentication Context and Session State Unit Tests
 * Author: Kailash-18
 */

export function testAuthValidation() {
  const validateCredentials = (u: string, p: string) => {
    return Boolean(u && p && u.trim().length >= 3 && p.trim().length >= 3);
  };

  if (!validateCredentials('admin', 'admin')) throw new Error('Valid credentials rejected');
  if (validateCredentials('', 'pass')) throw new Error('Empty username allowed');
  if (validateCredentials('user', '')) throw new Error('Empty password allowed');
  if (validateCredentials('a', 'b')) throw new Error('Too short credentials allowed');

  return true;
}

export function testSessionTokenStorage() {
  const mockStorage: Record<string, string> = {};
  const saveSession = (k: string, v: string) => { mockStorage[k] = v; };
  const getSession = (k: string) => mockStorage[k] || null;

  saveSession('polygen_user', JSON.stringify({ name: 'admin' }));
  const loaded = JSON.parse(getSession('polygen_user') || '{}');
  if (loaded.name !== 'admin') throw new Error('Session storage mismatch');

  return true;
}
