import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Register from './pages/Register';
import CheckEligibility from './pages/CheckEligibility';
import LoanDetails from './pages/LoanDetails';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/register" element={<Register />} />
        <Route path="/check-eligibility" element={<CheckEligibility />} />
        <Route path="/loan/:loanId" element={<LoanDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
