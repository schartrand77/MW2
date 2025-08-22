import { expect, test } from 'vitest';
import { loadPlugins } from './index';

test('loads plugins', async () => {
  await loadPlugins(['./samplePlugin.ts']);
  expect((window as any).__samplePluginLoaded).toBe(true);
});
