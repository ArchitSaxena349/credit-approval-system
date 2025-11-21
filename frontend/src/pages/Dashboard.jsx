import { useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import { UserPlus, Calculator, Search, ArrowRight, CreditCard } from 'lucide-react';

export default function Dashboard() {
    const [customerId, setCustomerId] = useState('');
    const [loans, setLoans] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!customerId) return;

        setLoading(true);
        setError(null);
        setLoans(null);

        try {
            const data = await api.getCustomerLoans(customerId);
            setLoans(data);
        } catch (err) {
            setError('No loans found for this customer ID');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
            <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
                <h1 style={{ fontSize: '3.5rem', fontWeight: '800', marginBottom: '1rem', background: 'linear-gradient(to right, var(--primary), var(--secondary))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
                    Credit Approval System
                </h1>
                <p style={{ fontSize: '1.25rem', color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto' }}>
                    Advanced AI-powered credit scoring and loan management platform.
                </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem', marginBottom: '4rem' }}>
                <Link to="/register" className="card" style={{ textDecoration: 'none', transition: 'transform 0.2s', cursor: 'pointer' }}>
                    <div style={{ width: '48px', height: '48px', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)', marginBottom: '1.5rem' }}>
                        <UserPlus size={24} />
                    </div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Register Customer</h3>
                    <p style={{ color: 'var(--text-muted)' }}>Create a new customer profile and calculate credit limit instantly.</p>
                </Link>

                <Link to="/check-eligibility" className="card" style={{ textDecoration: 'none', transition: 'transform 0.2s', cursor: 'pointer' }}>
                    <div style={{ width: '48px', height: '48px', background: 'rgba(236, 72, 153, 0.1)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--secondary)', marginBottom: '1.5rem' }}>
                        <Calculator size={24} />
                    </div>
                    <h3 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>Check Eligibility</h3>
                    <p style={{ color: 'var(--text-muted)' }}>Verify loan eligibility and get corrected interest rates.</p>
                </Link>
            </div>

            <div className="card">
                <h2 style={{ fontSize: '1.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <Search size={24} /> Find Customer Loans
                </h2>

                <form onSubmit={handleSearch} style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
                    <input
                        type="number"
                        placeholder="Enter Customer ID"
                        className="input-field"
                        value={customerId}
                        onChange={(e) => setCustomerId(e.target.value)}
                        style={{ maxWidth: '300px' }}
                    />
                    <button type="submit" className="btn btn-primary" disabled={loading}>
                        {loading ? 'Searching...' : 'Search'}
                    </button>
                </form>

                {error && (
                    <div style={{ padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', color: 'var(--error)', borderRadius: '0.5rem' }}>
                        {error}
                    </div>
                )}

                {loans && (
                    <div style={{ display: 'grid', gap: '1rem' }}>
                        {loans.length === 0 ? (
                            <p style={{ color: 'var(--text-muted)' }}>No active loans found for this customer.</p>
                        ) : (
                            loans.map((loan) => (
                                <Link key={loan.loan_id} to={`/loan/${loan.loan_id}`} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.5rem', background: 'rgba(255,255,255,0.03)', borderRadius: '0.5rem', border: '1px solid transparent', transition: 'all 0.2s' }} className="loan-item">
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                                        <div style={{ padding: '0.75rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '0.5rem', color: 'var(--success)' }}>
                                            <CreditCard size={24} />
                                        </div>
                                        <div>
                                            <h4 style={{ fontSize: '1.125rem', marginBottom: '0.25rem' }}>Loan #{loan.loan_id}</h4>
                                            <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{loan.repayments_left} repayments left</p>
                                        </div>
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <div style={{ fontSize: '1.25rem', fontWeight: '600' }}>₹{parseFloat(loan.loan_amount).toLocaleString()}</div>
                                        <div style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>{loan.interest_rate}% Interest</div>
                                    </div>
                                </Link>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}
