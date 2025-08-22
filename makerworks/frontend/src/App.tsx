import { Link, Route, Routes } from 'react-router-dom';
import SignUp from './pages/SignUp';
import ThemeEditor from './pages/ThemeEditor';
import CommandPalette from './components/CommandPalette';

function Home() {
  return (
    <div>
      <h1>MakerWorks</h1>
      <Link to="/signup">Sign Up</Link>
    </div>
  );
}

export default function App() {
  return (
    <>
      <CommandPalette />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/theme" element={<ThemeEditor />} />
      </Routes>
    </>
  );
}
