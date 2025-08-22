import { describe, it, expect } from 'vitest';
import { toCSV, fromCSV } from './csv';

describe('csv utils', () => {
  it('round trips data', () => {
    const rows = [
      { id: '1', name: 'alpha' },
      { id: '2', name: 'beta' }
    ];
    const csv = toCSV(rows);
    expect(csv).toContain('id,name');
    const parsed = fromCSV(csv);
    expect(parsed).toEqual(rows);
  });
});
