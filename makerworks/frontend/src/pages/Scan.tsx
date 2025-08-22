import { useEffect, useRef, useState } from 'react';
import { BrowserMultiFormatReader } from '@zxing/browser';

export default function Scan() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [result, setResult] = useState<string | null>(null);

  useEffect(() => {
    if (!navigator.mediaDevices) return;
    const codeReader = new BrowserMultiFormatReader();
    let active = true;
    codeReader.decodeFromVideoDevice(undefined, videoRef.current!, (res) => {
      if (res && active) {
        const text = res.getText();
        setResult(text);
        fetch('/api/v1/inventory/moves', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sku: text, delta: 1 })
        });
        active = false;
        codeReader.reset();
      }
    });
    return () => {
      active = false;
      codeReader.reset();
    };
  }, []);

  return (
    <div>
      <h2>Scan Barcode</h2>
      <video ref={videoRef} />
      {result && <p>Scanned: {result}</p>}
    </div>
  );
}
