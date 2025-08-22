import { Link } from 'react-router-dom';
import Button from '../components/Button';

export default function SignUp() {
  return (
    <div>
      <h2>Sign Up</h2>
      <Button variant="primary">Create account</Button>
      <p>
        Already a member? <Link to="/signin">Sign In</Link>
      </p>
    </div>
  );
}
