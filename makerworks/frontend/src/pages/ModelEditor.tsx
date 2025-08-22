import { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import Button from '../components/Button';

export default function ModelEditor() {
  const mountRef = useRef<HTMLDivElement>(null);
  const { id } = useParams();
  const [color, setColor] = useState('#00ff00');

  useEffect(() => {
    if (typeof WebGLRenderingContext === 'undefined') return;
    let renderer: any;
    (async () => {
      const THREE = await import('three');
      const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js');
      const { STLLoader } = await import('three/examples/jsm/loaders/STLLoader.js');
      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(300, 300);
      mountRef.current?.appendChild(renderer.domElement);
      const controls = new OrbitControls(camera, renderer.domElement);
      camera.position.z = 5;
      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(5, 5, 5);
      scene.add(light);
      const loader = new STLLoader();
      loader.load(`/api/v1/models/${id}/file`, geometry => {
        const material = new THREE.MeshStandardMaterial({ color });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
        animate();
        function animate() {
          requestAnimationFrame(animate);
          controls.update();
          renderer.render(scene, camera);
        }
      });
    })();
    return () => renderer?.dispose();
  }, [id, color]);

  const save = async () => {
    await fetch(`/api/v1/models/${id}/color`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ color }),
    });
  };

  return (
    <div>
      <h2>Model Editor</h2>
      <div ref={mountRef} />
      <input type="color" value={color} onChange={e => setColor(e.target.value)} />
      <Button onClick={save}>Save</Button>
    </div>
  );
}
