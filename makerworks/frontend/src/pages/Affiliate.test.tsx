import { describe, expect, it, beforeAll } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Affiliate from './Affiliate';

const queryClient = new QueryClient();

beforeAll(() => {
  // @ts-ignore
  global.fetch = async () => ({ json: async () => ({ items: [] }) });
});

describe('Affiliate', () => {
  it('shows disclosure', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Affiliate />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText('Links may earn us commission.')).toBeDefined();
  });
});
