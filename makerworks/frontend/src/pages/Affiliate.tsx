import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Button from '../components/Button';

interface Item {
  title: string;
  url: string;
}

async function search(query: string): Promise<Item[]> {
  const res = await fetch(`/api/v1/amazon/search?q=${encodeURIComponent(query)}`);
  const data = await res.json();
  return data.items;
}

export default function Affiliate() {
  const [query, setQuery] = useState('');
  const { data, refetch } = useQuery({
    queryKey: ['affiliate', query],
    queryFn: () => search(query),
    enabled: false,
  });

  return (
    <div>
      <h2>Amazon Affiliate</h2>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Button onClick={() => refetch()}>Search</Button>
      <p>Links may earn us commission.</p>
      <ul>
        {data?.map((item) => (
          <li key={item.url}>
            <a href={item.url} target="_blank" rel="noopener noreferrer">
              {item.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
