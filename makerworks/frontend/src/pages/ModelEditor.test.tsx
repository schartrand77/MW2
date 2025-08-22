import { describe, expect, it } from 'vitest';
import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ModelEditor from './ModelEditor';

describe('ModelEditor', () => {
  it('renders color picker', () => {
    const { container } = render(
      <BrowserRouter>
        <ModelEditor />
      </BrowserRouter>
    );
    expect(container.querySelector('input[type="color"]')).toBeTruthy();
  });
});
