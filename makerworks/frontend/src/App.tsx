import { Link, Route, Routes } from 'react-router-dom';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';

function Home() {
  return (
    <div>
      <h1>MakerWorks</h1>
      <Link to="/signup">Sign Up</Link>
      <br />
      <Link to="/signin">Sign In</Link>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/signin" element={<SignIn />} />
    </Routes>
  );
}
