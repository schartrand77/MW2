import { useEffect, useState } from 'react';
import Skeleton from '../components/Skeleton';
import EmptyState from '../components/EmptyState';

export default function Home() {
  const [items, setItems] = useState<string[] | null>(null);

  useEffect(() => {
    fetch('/api/v1/system/ping').then(() => setItems([]));
  }, []);

  if (items === null) return <Skeleton height="2rem" />;
  if (items.length === 0) return <EmptyState message="Nothing here yet" />;

  return (
    <ul>
      {items.map((i) => (
        <li key={i}>{i}</li>
      ))}
    </ul>
  );
}
