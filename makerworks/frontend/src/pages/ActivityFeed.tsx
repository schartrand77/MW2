import { useQuery } from '@tanstack/react-query';

async function fetchActivity() {
  const res = await fetch('/api/v1/admin/activity');
  if (!res.ok) throw new Error('failed');
  return res.json();
}

export default function ActivityFeed() {
  const { data } = useQuery({ queryKey: ['activity'], queryFn: fetchActivity });
  return (
    <div>
      <h2>Activity Feed</h2>
      <ul>
        {data?.map((e: any) => (
          <li key={e.id}>{e.action}</li>
        ))}
      </ul>
    </div>
  );
}
