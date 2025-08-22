import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import * as Sentry from '@sentry/react';
import App from './App';
import './style.css';
import { loadPlugins } from './plugins';
import { registerSW } from 'virtual:pwa-register';
import { initTheme } from './state/theme';

Sentry.init({ dsn: import.meta.env.VITE_SENTRY_DSN || undefined });
await loadPlugins();
registerSW();
await initTheme();

const queryClient = new QueryClient();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>
);
