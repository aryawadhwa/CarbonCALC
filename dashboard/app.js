// API Base URL
const API_BASE = window.location.origin;

// Global state
let currentUser = null;
let authToken = null;
let footprintChart = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is logged in
    authToken = localStorage.getItem('authToken');
    if (authToken) {
        loadUserProfile();
        showSection('dashboard');
    } else {
        showSection('authSection');
    }

    // Show/hide corporate section based on user type
    document.getElementById('regUserType').addEventListener('change', (e) => {
        const orgGroup = document.getElementById('orgNameGroup');
        if (e.target.value !== 'individual') {
            orgGroup.style.display = 'block';
        } else {
            orgGroup.style.display = 'none';
        }
    });
});

// Authentication functions
function switchAuthTab(tab) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const tabs = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    
    if (tab === 'login') {
        loginForm.classList.add('active');
        registerForm.classList.remove('active');
    } else {
        loginForm.classList.remove('active');
        registerForm.classList.add('active');
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            localStorage.setItem('authToken', authToken);
            currentUser = data.user;
            showSection('dashboard');
            loadDashboard();
        } else {
            alert('Login failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function handleRegister(event) {
    event.preventDefault();
    const formData = {
        email: document.getElementById('regEmail').value,
        username: document.getElementById('regUsername').value,
        password: document.getElementById('regPassword').value,
        full_name: document.getElementById('regFullName').value,
        user_type: document.getElementById('regUserType').value,
        organization_name: document.getElementById('regOrgName').value || null
    };

    try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            switchAuthTab('login');
            document.getElementById('loginUsername').value = formData.username;
        } else {
            alert('Registration failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function logout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('authToken');
    showSection('authSection');
}

async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE}/api/auth/me`, {
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            // Show corporate section if user is corporation or institution
            const corporateSection = document.getElementById('corporateSection');
            if (currentUser.user_type !== 'individual') {
                corporateSection.style.display = 'block';
            }
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Navigation
function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(sectionId).classList.add('active');
    
    // Load section data
    if (sectionId === 'dashboard') {
        loadDashboard();
    } else if (sectionId === 'recommendations') {
        loadRecommendations();
    } else if (sectionId === 'history') {
        loadHistory();
    } else if (sectionId === 'profile') {
        loadProfile();
    }
}

// Dashboard
async function loadDashboard() {
    try {
        // Load analytics
        const analyticsResponse = await fetch(`${API_BASE}/api/analytics/summary`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (analyticsResponse.ok) {
            const analytics = await analyticsResponse.json();
            document.getElementById('latestFootprint').textContent = analytics.latest_footprint || '-';
            document.getElementById('avgFootprint').textContent = analytics.average_footprint || '-';
            document.getElementById('totalEntries').textContent = analytics.total_entries || '0';
            
            const trendElement = document.getElementById('trend');
            const trendLabel = document.getElementById('trendLabel');
            if (analytics.trend === 'decreasing') {
                trendElement.textContent = '📉';
                trendLabel.textContent = 'Decreasing';
            } else if (analytics.trend === 'increasing') {
                trendElement.textContent = '📈';
                trendLabel.textContent = 'Increasing';
            } else {
                trendElement.textContent = '➡️';
                trendLabel.textContent = 'Stable';
            }
        }
        
        // Load history for chart
        const historyResponse = await fetch(`${API_BASE}/api/entries?limit=12`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (historyResponse.ok) {
            const entries = await historyResponse.json();
            renderFootprintChart(entries);
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function renderFootprintChart(entries) {
    const ctx = document.getElementById('footprintChart');
    if (!ctx) return;
    
    const labels = entries.reverse().map(e => {
        const date = new Date(e.entry_date);
        return date.toLocaleDateString();
    });
    const data = entries.map(e => e.total_carbon_footprint);
    
    if (footprintChart) {
        footprintChart.destroy();
    }
    
    footprintChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Carbon Footprint (kg CO₂)',
                data: data,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Carbon Footprint Over Time'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'kg CO₂'
                    }
                }
            }
        }
    });
}

// Calculate footprint
async function handleCalculate(event) {
    event.preventDefault();
    
    const formData = {
        electricity_usage: parseFloat(document.getElementById('electricity_usage').value) || 0,
        gas_usage: parseFloat(document.getElementById('gas_usage').value) || 0,
        heating_oil: parseFloat(document.getElementById('heating_oil').value) || 0,
        vehicle_miles: parseFloat(document.getElementById('vehicle_miles').value) || 0,
        public_transport_km: parseFloat(document.getElementById('public_transport_km').value) || 0,
        flights_km: parseFloat(document.getElementById('flights_km').value) || 0,
        waste_produced: parseFloat(document.getElementById('waste_produced').value) || 0,
        recycling_rate: parseFloat(document.getElementById('recycling_rate').value) || 0,
        meat_consumption: parseFloat(document.getElementById('meat_consumption').value) || 0,
        vegetarian_meals: parseFloat(document.getElementById('vegetarian_meals').value) || 0,
        water_usage: parseFloat(document.getElementById('water_usage').value) || 0,
        employee_count: parseInt(document.getElementById('employee_count').value) || 1,
        office_space_sqm: parseFloat(document.getElementById('office_space_sqm').value) || 0,
        manufacturing_output: parseFloat(document.getElementById('manufacturing_output').value) || 0,
        supply_chain_distance: parseFloat(document.getElementById('supply_chain_distance').value) || 0,
        notes: document.getElementById('notes').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
            // Refresh dashboard and recommendations
            loadDashboard();
            loadRecommendations();
        } else {
            alert('Error: ' + (data.detail || 'Failed to calculate footprint'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function displayResults(data) {
    const footprint = data.footprint;
    const recommendations = data.recommendations;
    
    let html = `
        <div class="total-footprint">
            <div class="label">Total Carbon Footprint</div>
            <div class="value">${footprint.total.toLocaleString()} kg CO₂</div>
            <div style="margin-top: 0.5rem; font-size: 1rem;">
                ${footprint.per_person > 0 ? `Per Person: ${footprint.per_person.toLocaleString()} kg CO₂` : ''}
            </div>
        </div>
        
        <h4 style="margin-top: 2rem;">Breakdown by Category</h4>
        <div class="footprint-breakdown">
            <div class="breakdown-item">
                <div class="label">Energy</div>
                <div class="value">${footprint.energy} kg</div>
            </div>
            <div class="breakdown-item">
                <div class="label">Transportation</div>
                <div class="value">${footprint.transportation} kg</div>
            </div>
            <div class="breakdown-item">
                <div class="label">Waste</div>
                <div class="value">${footprint.waste} kg</div>
            </div>
            <div class="breakdown-item">
                <div class="label">Food</div>
                <div class="value">${footprint.food} kg</div>
            </div>
            <div class="breakdown-item">
                <div class="label">Water</div>
                <div class="value">${footprint.water} kg</div>
            </div>
            ${footprint.corporate > 0 ? `
            <div class="breakdown-item">
                <div class="label">Corporate</div>
                <div class="value">${footprint.corporate} kg</div>
            </div>
            ` : ''}
        </div>
    `;
    
    if (recommendations && recommendations.length > 0) {
        html += `<h4 style="margin-top: 2rem;">Top Recommendations</h4>`;
        recommendations.slice(0, 3).forEach(rec => {
            html += `
                <div class="recommendation-card">
                    <h4>${rec.title}</h4>
                    <p>${rec.description}</p>
                    <div class="recommendation-meta">
                        <span class="meta-badge badge-impact-${rec.impact_rating >= 4 ? 'high' : 'medium'}">
                            Impact: ${rec.impact_rating}/5
                        </span>
                        <span class="meta-badge badge-difficulty-${rec.difficulty}">
                            ${rec.difficulty.charAt(0).toUpperCase() + rec.difficulty.slice(1)}
                        </span>
                        <span class="meta-badge" style="background: #dbeafe; color: #1e40af;">
                            Reduce: ${rec.estimated_reduction} kg CO₂
                        </span>
                    </div>
                </div>
            `;
        });
    }
    
    document.getElementById('resultsContent').innerHTML = html;
}

// Recommendations
async function loadRecommendations() {
    try {
        const response = await fetch(`${API_BASE}/api/recommendations`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const recommendations = await response.json();
            displayRecommendations(recommendations);
        } else {
            document.getElementById('recommendationsContent').innerHTML = 
                '<p>No recommendations available. Calculate your carbon footprint first!</p>';
        }
    } catch (error) {
        document.getElementById('recommendationsContent').innerHTML = 
            '<p>Error loading recommendations.</p>';
    }
}

function displayRecommendations(recommendations) {
    if (recommendations.length === 0) {
        document.getElementById('recommendationsContent').innerHTML = 
            '<p>No recommendations available. Calculate your carbon footprint first!</p>';
        return;
    }
    
    let html = '';
    recommendations.forEach(rec => {
        html += `
            <div class="recommendation-card">
                <h4>${rec.title}</h4>
                <p>${rec.description}</p>
                <div class="recommendation-meta">
                    <span class="meta-badge badge-impact-${rec.impact_rating >= 4 ? 'high' : 'medium'}">
                        Impact: ${rec.impact_rating}/5
                    </span>
                    <span class="meta-badge badge-difficulty-${rec.difficulty}">
                        ${rec.difficulty.charAt(0).toUpperCase() + rec.difficulty.slice(1)}
                    </span>
                    <span class="meta-badge" style="background: #dbeafe; color: #1e40af;">
                        Reduce: ${rec.estimated_reduction} kg CO₂/year
                    </span>
                    <span class="meta-badge" style="background: #e0e7ff; color: #3730a3;">
                        Cost: ${rec.cost_estimate || 'N/A'}
                    </span>
                </div>
            </div>
        `;
    });
    
    document.getElementById('recommendationsContent').innerHTML = html;
}

// History
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/entries?limit=20`, {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        
        if (response.ok) {
            const entries = await response.json();
            displayHistory(entries);
        } else {
            document.getElementById('historyContent').innerHTML = 
                '<p>No history available.</p>';
        }
    } catch (error) {
        document.getElementById('historyContent').innerHTML = 
            '<p>Error loading history.</p>';
    }
}

function displayHistory(entries) {
    if (entries.length === 0) {
        document.getElementById('historyContent').innerHTML = 
            '<p>No entries found. Calculate your carbon footprint to get started!</p>';
        return;
    }
    
    let html = '';
    entries.forEach(entry => {
        const date = new Date(entry.entry_date);
        const breakdown = entry.category_breakdown || {};
        
        html += `
            <div class="history-entry">
                <div class="history-entry-header">
                    <h4>Entry #${entry.id}</h4>
                    <div class="date">${date.toLocaleDateString()} ${date.toLocaleTimeString()}</div>
                </div>
                <div class="total-footprint" style="background: linear-gradient(135deg, #10b981, #3b82f6); margin: 1rem 0;">
                    <div class="value" style="font-size: 2rem;">${entry.total_carbon_footprint.toLocaleString()} kg CO₂</div>
                </div>
                <div class="footprint-breakdown">
                    ${Object.entries(breakdown).filter(([k]) => k !== 'total' && k !== 'per_person').map(([key, value]) => `
                        <div class="breakdown-item">
                            <div class="label">${key.charAt(0).toUpperCase() + key.slice(1)}</div>
                            <div class="value">${value} kg</div>
                        </div>
                    `).join('')}
                </div>
                ${entry.notes ? `<p style="margin-top: 1rem; color: var(--text-secondary);"><strong>Notes:</strong> ${entry.notes}</p>` : ''}
            </div>
        `;
    });
    
    document.getElementById('historyContent').innerHTML = html;
}

// Profile
async function loadProfile() {
    if (!currentUser) {
        await loadUserProfile();
    }
    
    if (currentUser) {
        document.getElementById('profileContent').innerHTML = `
            <div class="form-section">
                <h3>Profile Information</h3>
                <div class="form-group">
                    <label>Full Name</label>
                    <input type="text" value="${currentUser.full_name || ''}" disabled>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" value="${currentUser.email || ''}" disabled>
                </div>
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" value="${currentUser.username || ''}" disabled>
                </div>
                <div class="form-group">
                    <label>User Type</label>
                    <input type="text" value="${currentUser.user_type.charAt(0).toUpperCase() + currentUser.user_type.slice(1)}" disabled>
                </div>
                ${currentUser.organization_name ? `
                <div class="form-group">
                    <label>Organization Name</label>
                    <input type="text" value="${currentUser.organization_name}" disabled>
                </div>
                ` : ''}
            </div>
        `;
    }
}

