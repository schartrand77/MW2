import type { CSSProperties } from 'react';

export default function Skeleton({ width = '100%', height = '1rem' }: { width?: string; height?: string }) {
  const style: CSSProperties = { width, height };
  return <div className="skeleton" style={style} />;
}
