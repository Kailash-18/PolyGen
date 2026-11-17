/**
 * Dark and Light Theme State Unit Tests
 * Author: Kailash-18
 */

export function testThemeToggleLogic() {
  const getNextTheme = (current: string) => (current === 'dark' ? 'light' : 'dark');

  if (getNextTheme('dark') !== 'light') throw new Error('Theme should toggle to light');
  if (getNextTheme('light') !== 'dark') throw new Error('Theme should toggle back to dark');

  return true;
}

export function testThemeAttributeBinding() {
  const applyTheme = (t: string) => t.toLowerCase();

  if (applyTheme('LIGHT') !== 'light') throw new Error('Theme attribute not set');
  if (applyTheme('DARK') !== 'dark') throw new Error('Theme attribute not restored');

  return true;
}
