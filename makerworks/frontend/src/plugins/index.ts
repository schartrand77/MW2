export type ClientPlugin = { setup?: () => void };

export async function loadPlugins(list?: string[]) {
  const modules =
    list ??
    ((import.meta.env.VITE_PLUGINS as string | undefined)?.split(',').map(s => s.trim()).filter(Boolean) ?? []);
  for (const mod of modules) {
    try {
      const plugin: ClientPlugin = await import(/* @vite-ignore */ mod);
      plugin.setup?.();
    } catch (err) {
      console.error('Failed to load plugin', mod, err);
    }
  }
}
