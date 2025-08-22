import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import PrinterAdmin from './PrinterAdmin';

describe('PrinterAdmin', () => {
  it('shows input fields', () => {
    render(
      <BrowserRouter>
        <PrinterAdmin />
      </BrowserRouter>
    );
    expect(screen.getByLabelText('Bambu API Key')).toBeDefined();
    expect(screen.getByLabelText('OctoPrint URL')).toBeDefined();
  });
});

