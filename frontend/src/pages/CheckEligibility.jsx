import { useState } from 'react';
import { api } from '../services/api';
import { Calculator, CheckCircle, XCircle, ArrowRight, DollarSign } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export default function CheckEligibility() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        customer_id: '',
        loan_amount: '',
        interest_rate: '',
        tenure: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [applying, setApplying] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleCheck = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const data = await api.checkEligibility({
                customer_id: parseInt(formData.customer_id),
                loan_amount: parseFloat(formData.loan_amount),
                interest_rate: parseFloat(formData.interest_rate),
                tenure: parseInt(formData.tenure)
            });
            setResult(data);
        } catch (error) {
            alert('Error checking eligibility: ' + (error.message || JSON.stringify(error.data)));
        } finally {
            setLoading(false);
        }
    };

    const handleApply = async () => {
        setApplying(true);
        try {
            const data = await api.createLoan({
                customer_id: parseInt(formData.customer_id),
                loan_amount: parseFloat(formData.loan_amount),
                interest_rate: parseFloat(formData.interest_rate),
                tenure: parseInt(formData.tenure)
            });

            if (data.loan_approved) {
                navigate(`/loan/${data.loan_id}`);
            } else {
                alert('Loan application rejected: ' + data.message);
            }
        } catch (error) {
            alert('Error creating loan: ' + (error.message || JSON.stringify(error.data)));
        } finally {
            setApplying(false);
        }
    };

    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
            <div className="card" style={{ maxWidth: '800px', margin: '0 auto' }}>
                <div className="page-header">
                    <h1 className="page-title">Check Eligibility</h1>
                    <p className="page-subtitle">Calculate loan terms and apply instantly</p>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: result ? '1fr 1fr' : '1fr', gap: '2rem' }}>
                    <form onSubmit={handleCheck}>
                        <div className="input-group">
                            <label className="input-label">Customer ID</label>
                            <input
                                type="number"
                                name="customer_id"
                                className="input-field"
                                required
                                value={formData.customer_id}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">Loan Amount (₹)</label>
                            <input
                                type="number"
                                name="loan_amount"
                                className="input-field"
                                required
                                value={formData.loan_amount}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">Interest Rate (%)</label>
                            <input
                                type="number"
                                step="0.1"
                                name="interest_rate"
                                className="input-field"
                                required
                                value={formData.interest_rate}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">Tenure (Months)</label>
                            <input
                                type="number"
                                name="tenure"
                                className="input-field"
                                required
                                value={formData.tenure}
                                onChange={handleChange}
                            />
                        </div>

                        <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                            {loading ? 'Checking...' : (
                                <>
                                    <Calculator size={20} />
                                    Check Eligibility
                                </>
                            )}
                        </button>
                    </form>

                    {result && (
                        <div style={{ background: 'var(--background)', padding: '1.5rem', borderRadius: '0.5rem', border: '1px solid var(--border)' }}>
                            <h3 style={{ fontSize: '1.25rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                {result.approval ? (
                                    <span style={{ color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <CheckCircle size={24} /> Eligible
                                    </span>
                                ) : (
                                    <span style={{ color: 'var(--error)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <XCircle size={24} /> Not Eligible
                                    </span>
                                )}
                            </h3>

                            <div style={{ display: 'grid', gap: '1rem', marginBottom: '2rem' }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', borderRadius: '0.25rem' }}>
                                    <span style={{ color: 'var(--text-muted)' }}>Interest Rate</span>
                                    <span style={{ fontWeight: '600' }}>{result.corrected_interest_rate}%</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', borderRadius: '0.25rem' }}>
                                    <span style={{ color: 'var(--text-muted)' }}>Monthly EMI</span>
                                    <span style={{ fontWeight: '600' }}>₹{result.monthly_installment.toLocaleString()}</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem', background: 'rgba(255,255,255,0.05)', borderRadius: '0.25rem' }}>
                                    <span style={{ color: 'var(--text-muted)' }}>Tenure</span>
                                    <span style={{ fontWeight: '600' }}>{result.tenure} months</span>
                                </div>
                            </div>

                            {result.approval && (
                                <button
                                    onClick={handleApply}
                                    className="btn btn-primary"
                                    style={{ width: '100%', background: 'var(--success)' }}
                                    disabled={applying}
                                >
                                    {applying ? 'Processing...' : (
                                        <>
                                            <DollarSign size={20} />
                                            Apply for Loan
                                        </>
                                    )}
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
