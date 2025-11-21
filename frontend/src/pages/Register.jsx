import { useState } from 'react';
import { api } from '../services/api';
import { UserPlus, CheckCircle, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Register() {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        age: '',
        monthly_income: '',
        phone_number: ''
    });
    const [status, setStatus] = useState({ type: '', message: '', data: null });
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setStatus({ type: '', message: '', data: null });

        try {
            const data = await api.registerCustomer({
                ...formData,
                age: parseInt(formData.age),
                monthly_income: parseInt(formData.monthly_income)
            });
            setStatus({ type: 'success', message: 'Customer registered successfully!', data });
        } catch (error) {
            setStatus({
                type: 'error',
                message: error.data ? JSON.stringify(error.data) : 'Registration failed. Please try again.'
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container" style={{ paddingTop: '4rem', paddingBottom: '4rem' }}>
            <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
                <div className="page-header">
                    <h1 className="page-title">Register Customer</h1>
                    <p className="page-subtitle">Create a new customer profile</p>
                </div>

                {status.type === 'success' ? (
                    <div style={{ textAlign: 'center', padding: '2rem 0' }}>
                        <div style={{ color: 'var(--success)', marginBottom: '1rem' }}>
                            <CheckCircle size={64} style={{ margin: '0 auto' }} />
                        </div>
                        <h2 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Registration Successful!</h2>
                        <div style={{ background: 'rgba(16, 185, 129, 0.1)', padding: '1.5rem', borderRadius: '0.5rem', marginBottom: '2rem', textAlign: 'left' }}>
                            <p><strong>Customer ID:</strong> {status.data.customer_id}</p>
                            <p><strong>Name:</strong> {status.data.name}</p>
                            <p><strong>Approved Limit:</strong> ₹{status.data.approved_limit.toLocaleString()}</p>
                        </div>
                        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
                            <Link to="/" className="btn btn-outline">Back to Home</Link>
                            <Link to="/check-eligibility" className="btn btn-primary">Check Loan Eligibility</Link>
                        </div>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit}>
                        {status.type === 'error' && (
                            <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--error)', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                <AlertCircle size={20} />
                                <span>{status.message}</span>
                            </div>
                        )}

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div className="input-group">
                                <label className="input-label">First Name</label>
                                <input
                                    type="text"
                                    name="first_name"
                                    className="input-field"
                                    required
                                    value={formData.first_name}
                                    onChange={handleChange}
                                />
                            </div>
                            <div className="input-group">
                                <label className="input-label">Last Name</label>
                                <input
                                    type="text"
                                    name="last_name"
                                    className="input-field"
                                    required
                                    value={formData.last_name}
                                    onChange={handleChange}
                                />
                            </div>
                        </div>

                        <div className="input-group">
                            <label className="input-label">Age</label>
                            <input
                                type="number"
                                name="age"
                                className="input-field"
                                required
                                value={formData.age}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">Monthly Income (₹)</label>
                            <input
                                type="number"
                                name="monthly_income"
                                className="input-field"
                                required
                                value={formData.monthly_income}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="input-group">
                            <label className="input-label">Phone Number</label>
                            <input
                                type="tel"
                                name="phone_number"
                                className="input-field"
                                required
                                value={formData.phone_number}
                                onChange={handleChange}
                            />
                        </div>

                        <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={loading}>
                            {loading ? 'Registering...' : (
                                <>
                                    <UserPlus size={20} />
                                    Register Customer
                                </>
                            )}
                        </button>
                    </form>
                )}
            </div>
        </div>
    );
}
