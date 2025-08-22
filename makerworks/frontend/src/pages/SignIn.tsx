import { Link } from 'react-router-dom';
import Button from '../components/Button';

export default function SignIn() {
  return (
    <div>
      <h2>Sign In</h2>
      <Button variant="primary">Sign In</Button>
      <p>
        Need an account? <Link to="/signup">Sign Up</Link>
      </p>
    </div>
  );
}
