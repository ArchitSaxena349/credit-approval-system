const BASE_URL = 'https://credit-approval-system-jbui.onrender.com';

export const api = {
  // Customer Registration
  registerCustomer: async (data) => {
    const response = await fetch(`${BASE_URL}/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  // Check Loan Eligibility
  checkEligibility: async (data) => {
    const response = await fetch(`${BASE_URL}/check-eligibility/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  // Create Loan
  createLoan: async (data) => {
    const response = await fetch(`${BASE_URL}/create-loan/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  // View Loan Details
  getLoanDetails: async (loanId) => {
    const response = await fetch(`${BASE_URL}/view-loan/${loanId}/`);
    return handleResponse(response);
  },

  // View Customer Loans
  getCustomerLoans: async (customerId) => {
    const response = await fetch(`${BASE_URL}/view-loans/${customerId}/`);
    return handleResponse(response);
  }
};

async function handleResponse(response) {
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    const data = await response.json();
    if (!response.ok) {
      throw { status: response.status, data };
    }
    return data;
  }
  if (!response.ok) {
    throw { status: response.status, message: response.statusText };
  }
  return response.text();
}
