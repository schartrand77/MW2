import create from 'zustand';

interface ThemeState {
  tokens: Record<string, string>;
  load: () => Promise<void>;
  setTokens: (t: Record<string, string>) => void;
}

function applyTokens(tokens: Record<string, string>) {
  const root = document.documentElement;
  for (const [k, v] of Object.entries(tokens)) {
    root.style.setProperty(`--${k}`, v);
  }
}

export const useThemeStore = create<ThemeState>((set) => ({
  tokens: {},
  load: async () => {
    const res = await fetch('/api/v1/themes/default');
    const data = await res.json();
    applyTokens(data.tokens);
    set({ tokens: data.tokens });
  },
  setTokens: (tokens) => {
    applyTokens(tokens);
    set({ tokens });
  },
}));

export async function initTheme() {
  await useThemeStore.getState().load();
}
