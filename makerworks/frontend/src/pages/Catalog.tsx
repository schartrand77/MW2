import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';

interface Variant {
  id: string;
  name: string;
  price_cents: number;
}
interface Product {
  id: string;
  name: string;
  variants: Variant[];
}

async function fetchProducts(): Promise<Product[]> {
  const res = await fetch('/api/v1/products');
  return res.json();
}

export default function Catalog() {
  const { data } = useQuery({ queryKey: ['products'], queryFn: fetchProducts });
  return (
    <div>
      <nav>
        <Link to="/catalog">Catalog</Link> | <Link to="/affiliate">Affiliate</Link>
      </nav>
      <h2>Catalog</h2>
      {data?.map((p) => (
        <div key={p.id}>
          <Link to={`/products/${p.id}`}>{p.name}</Link>
        </div>
      ))}
    </div>
  );
}
