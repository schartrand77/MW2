import { BrowserRouter } from 'react-router-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ThemeEditor from './ThemeEditor';
import { useThemeStore } from '../state/theme';

vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ json: async () => ({}) } as any));

function setup() {
  useThemeStore.setState({ tokens: { 'mw-green': '#00ff85', 'mw-red': '#ff0040', 'mw-text': '#ffffff', 'mw-bg': '#1b1b1b' } });
  render(
    <BrowserRouter>
      <ThemeEditor />
    </BrowserRouter>
  );
}

describe('ThemeEditor', () => {
  it('saves updated colors', async () => {
    setup();
    const greenInput = screen.getByLabelText('mw-green') as HTMLInputElement;
    fireEvent.change(greenInput, { target: { value: '#123456' } });
    fireEvent.click(screen.getByText('Save'));
    await new Promise((r) => setTimeout(r, 0));
    expect(useThemeStore.getState().tokens['mw-green']).toBe('#123456');
  });
});
