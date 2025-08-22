import { describe, it, expect, vi } from 'vitest';
import { initTheme, useThemeStore } from './theme';

describe('theme store', () => {
  it('loads tokens and applies css vars', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: async () => ({ tokens: { 'mw-green': '#00ff00' } }) } as any));
    await initTheme();
    expect(useThemeStore.getState().tokens['mw-green']).toBe('#00ff00');
    expect(getComputedStyle(document.documentElement).getPropertyValue('--mw-green').trim()).toBe('#00ff00');
  });
});
