import { describe, expect, it, beforeAll } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Catalog from './Catalog';

const queryClient = new QueryClient();

beforeAll(() => {
  // @ts-ignore
  global.fetch = async () => ({ json: async () => [] });
});

describe('Catalog', () => {
  it('renders heading', () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <Catalog />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText('Catalog')).toBeDefined();
  });
});
