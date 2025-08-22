import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface Command {
  name: string;
  action: () => void;
}

export default function CommandPalette() {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');

  const commands: Command[] = [
    { name: 'Home', action: () => navigate('/') },
    { name: 'Theme Editor', action: () => navigate('/theme') },
  ];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setOpen((o) => !o);
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, []);

  if (!open) return null;

  const filtered = commands.filter((c) => c.name.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="cmdk-overlay">
      <div className="cmdk-panel">
        <input
          autoFocus
          placeholder="Type a command"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <ul>
          {filtered.map((c) => (
            <li key={c.name}>
              <button
                onClick={() => {
                  c.action();
                  setOpen(false);
                }}
              >
                {c.name}
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
