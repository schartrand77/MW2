import { render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import Home from './Home';

describe('Home', () => {
  it('shows skeleton then empty state', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({} as any);
    render(<Home />);
    expect(document.querySelector('.skeleton')).toBeTruthy();
    await waitFor(() => screen.getByText('Nothing here yet'));
  });
});
