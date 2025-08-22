import { ErrorBoundary as SentryBoundary } from '@sentry/react';
import type { ReactNode } from 'react';

export default function ErrorBoundary({ children }: { children: ReactNode }) {
  return (
    <SentryBoundary fallback={<div role="alert">Something went wrong</div>}>
      {children}
    </SentryBoundary>
  );
}
