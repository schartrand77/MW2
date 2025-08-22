import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import Scan from './Scan';

describe('Scan', () => {
  it('renders heading', () => {
    render(<Scan />);
    expect(screen.getByText('Scan Barcode')).toBeDefined();
  });
});
