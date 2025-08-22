import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ActivityFeed from './ActivityFeed';

describe('ActivityFeed', () => {
  it('renders heading', () => {
    const qc = new QueryClient();
    render(
      <QueryClientProvider client={qc}>
        <ActivityFeed />
      </QueryClientProvider>
    );
    expect(screen.getByText('Activity Feed')).toBeDefined();
  });
});
