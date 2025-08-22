import { Route, Routes } from 'react-router-dom';
import SignUp from './pages/SignUp';
import ThemeEditor from './pages/ThemeEditor';
import Home from './pages/Home';
import CommandPalette from './components/CommandPalette';
import ErrorBoundary from './components/ErrorBoundary';

export default function App() {
  return (
    <ErrorBoundary>
      <CommandPalette />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<SignUp />} />
        <Route path="/theme" element={<ThemeEditor />} />
      </Routes>
    </ErrorBoundary>
  );
}
