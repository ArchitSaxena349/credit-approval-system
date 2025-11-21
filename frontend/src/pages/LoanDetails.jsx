import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import { FileText, User, Calendar, DollarSign, ArrowLeft } from 'lucide-react';

export default function LoanDetails() {
    const { loanId } = useParams();
    const [loan, setLoan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLoan = async () => {
            try {
                const data = await api.getLoanDetails(loanId);
                setLoan(data);
            } catch (err) {
                setError('Failed to load loan details');
            } finally {
                setLoading(false);
            }
        };
        fetchLoan();
    }, [loanId]);

    if (loading) return <div className="container" style={{ paddingTop: '4rem', textAlign: 'center' }}>Loading...</div>;
    if (error) return <div className="container" style={{ paddingTop: '4rem', textAlign: 'center', color: 'var(--error)' }}>{error}</div>;
    if (!loan) return null;

    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
            <Link to="/" className="btn btn-outline" style={{ marginBottom: '2rem' }}>
                <ArrowLeft size={20} /> Back to Dashboard
            </Link>

            <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
                <div className="page-header">
                    <h1 className="page-title">Loan #{loan.loan_id}</h1>
                    <p className="page-subtitle">Loan Details and Repayment Schedule</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '0.5rem' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--primary)' }}>
                            <User size={20} /> Customer Details
                        </h3>
                        <div style={{ display: 'grid', gap: '0.5rem' }}>
                            <p><strong>Name:</strong> {loan.customer.first_name} {loan.customer.last_name}</p>
                            <p><strong>Age:</strong> {loan.customer.age}</p>
                            <p><strong>Phone:</strong> {loan.customer.phone_number}</p>
                        </div>
                    </div>

                    <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1.5rem', borderRadius: '0.5rem' }}>
                        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem', color: 'var(--secondary)' }}>
                            <FileText size={20} /> Loan Terms
                        </h3>
                        <div style={{ display: 'grid', gap: '0.5rem' }}>
                            <p><strong>Amount:</strong> ₹{parseFloat(loan.loan_amount).toLocaleString()}</p>
                            <p><strong>Interest Rate:</strong> {loan.interest_rate}%</p>
                            <p><strong>Tenure:</strong> {loan.tenure} months</p>
                        </div>
                    </div>
                </div>

                <div style={{ background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(236, 72, 153, 0.1))', padding: '2rem', borderRadius: '0.5rem', textAlign: 'center' }}>
                    <h2 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', color: 'var(--text-muted)' }}>Monthly Repayment</h2>
                    <div style={{ fontSize: '3rem', fontWeight: '700', color: 'var(--text)' }}>
                        ₹{parseFloat(loan.monthly_repayment).toLocaleString()}
                    </div>
                </div>
            </div>
        </div>
    );
}
