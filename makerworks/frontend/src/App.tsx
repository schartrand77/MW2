import { Link, Route, Routes } from 'react-router-dom';
import SignUp from './pages/SignUp';
import SignIn from './pages/SignIn';
import Catalog from './pages/Catalog';
import Product from './pages/Product';
import Cart from './pages/Cart';
import CheckoutSuccess from './pages/CheckoutSuccess';
import CheckoutCancel from './pages/CheckoutCancel';
import Affiliate from './pages/Affiliate';
import Scan from './pages/Scan';
import PrinterAdmin from './pages/PrinterAdmin';
import ModelEditor from './pages/ModelEditor';
import ActivityFeed from './pages/ActivityFeed';

function Home() {
  return (
    <div>
      <h1>MakerWorks</h1>
      <Link to="/signup">Sign Up</Link>
      <br />
      <Link to="/signin">Sign In</Link>
      <br />
      <Link to="/catalog">Catalog</Link>
      <br />
      <Link to="/cart">Cart</Link>
      <br />
      <Link to="/affiliate">Affiliate</Link>
      <br />
      <Link to="/scan">Scan</Link>
      <br />
      <Link to="/admin/printers">Printers</Link>
      <br />
      <Link to="/models/demo/edit">Model Editor</Link>
      <br />
      <Link to="/admin/activity">Activity</Link>
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/signin" element={<SignIn />} />
      <Route path="/catalog" element={<Catalog />} />
      <Route path="/products/:id" element={<Product />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/affiliate" element={<Affiliate />} />
      <Route path="/scan" element={<Scan />} />
      <Route path="/admin/printers" element={<PrinterAdmin />} />
      <Route path="/models/:id/edit" element={<ModelEditor />} />
      <Route path="/admin/activity" element={<ActivityFeed />} />
      <Route path="/checkout/success" element={<CheckoutSuccess />} />
      <Route path="/checkout/cancel" element={<CheckoutCancel />} />
    </Routes>
  );
}
