import { useState, FormEvent } from 'react';
import Button from '../components/Button';

export default function PrinterAdmin() {
  const [bambuKey, setBambuKey] = useState('');
  const [octoUrl, setOctoUrl] = useState('');
  const [octoKey, setOctoKey] = useState('');

  const submit = (e: FormEvent) => {
    e.preventDefault();
    // stub save
    console.log({ bambuKey, octoUrl, octoKey });
  };

  return (
    <form onSubmit={submit}>
      <div>
        <label>
          Bambu API Key
          <input value={bambuKey} onChange={(e) => setBambuKey(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          OctoPrint URL
          <input value={octoUrl} onChange={(e) => setOctoUrl(e.target.value)} />
        </label>
      </div>
      <div>
        <label>
          OctoPrint API Key
          <input value={octoKey} onChange={(e) => setOctoKey(e.target.value)} />
        </label>
      </div>
      <Button variant="primary" type="submit">
        Save
      </Button>
    </form>
  );
}

