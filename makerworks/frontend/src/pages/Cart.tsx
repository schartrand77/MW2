import { useQuery } from '@tanstack/react-query';
import Button from '../components/Button';

interface CartItem {
  id: string;
  product_variant_id: string;
  quantity: number;
}
interface Cart {
  id: string;
  items: CartItem[];
}

async function fetchCart(): Promise<Cart> {
  const res = await fetch('/api/v1/cart');
  return res.json();
}

async function checkout(): Promise<void> {
  const res = await fetch('/api/v1/checkout/session', { method: 'POST' });
  const data = await res.json();
  window.location.href = data.url;
}

export default function CartPage() {
  const { data } = useQuery({ queryKey: ['cart'], queryFn: fetchCart });
  const count = data?.items.reduce((s, i) => s + i.quantity, 0) ?? 0;
  return (
    <div>
      <h2>Cart</h2>
      <p>Items: {count}</p>
      <Button onClick={() => checkout()}>Checkout</Button>
    </div>
  );
}
