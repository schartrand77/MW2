import { useState } from 'react';
import Button from '../components/Button';
import { useThemeStore } from '../state/theme';

const KEYS = ['mw-green', 'mw-red', 'mw-text', 'mw-bg'];

export default function ThemeEditor() {
  const tokens = useThemeStore((s) => s.tokens);
  const setTokens = useThemeStore((s) => s.setTokens);
  const [local, setLocal] = useState(tokens);

  const handleChange = (key: string, value: string) => {
    setLocal({ ...local, [key]: value });
  };

  const save = async () => {
    await fetch('/api/v1/themes/default', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tokens: local }),
    });
    setTokens(local);
  };

  return (
    <div>
      <h2>Theme Editor</h2>
      {KEYS.map((k) => (
        <div key={k}>
          <label>
            {k}
            <input type="color" value={local[k] || '#000000'} onChange={(e) => handleChange(k, e.target.value)} />
          </label>
        </div>
      ))}
      <Button onClick={save}>Save</Button>
    </div>
  );
}
