import { useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import Button from '../components/Button';

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

async function fetchProduct(id: string): Promise<Product> {
  const res = await fetch(`/api/v1/products/${id}`);
  return res.json();
}

async function addToCart(variantId: string) {
  await fetch('/api/v1/cart/items', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_variant_id: variantId, quantity: 1 })
  });
}

export default function ProductPage() {
  const { id = '' } = useParams();
  const queryClient = useQueryClient();
  const { data } = useQuery({ queryKey: ['product', id], queryFn: () => fetchProduct(id) });
  const mutation = useMutation({
    mutationFn: addToCart,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['cart'] })
  });
  if (!data) return <div>Loading...</div>;
  const variant = data.variants[0];
  return (
    <div>
      <h2>{data.name}</h2>
      {variant && (
        <Button onClick={() => mutation.mutate(variant.id)}>Add to Cart</Button>
      )}
    </div>
  );
}
