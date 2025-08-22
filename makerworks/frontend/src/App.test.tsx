import { describe, expect, it } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { vi } from 'vitest';

describe('App', () => {
  it('renders home page', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({} as any);
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    await waitFor(() => screen.getByText('Nothing here yet'));
  });
});
