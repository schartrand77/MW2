import { BrowserRouter } from 'react-router-dom';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CommandPalette from './CommandPalette';

function setup() {
  render(
    <BrowserRouter>
      <CommandPalette />
    </BrowserRouter>
  );
}

describe('CommandPalette', () => {
  it('opens with ctrl+k', async () => {
    setup();
    const event = new KeyboardEvent('keydown', { key: 'k', ctrlKey: true });
    window.dispatchEvent(event);
    expect(await screen.findByPlaceholderText('Type a command')).toBeDefined();
  });
});
