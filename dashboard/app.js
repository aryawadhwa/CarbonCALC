// app.js - Clean, modular, and maintainable
const API_BASE = window.location.origin;

const Auth = {
    token: localStorage.getItem('authToken'),
    user: null,

    async login(e) {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value.trim();
        const password = document.getElementById('loginPassword').value;

        try {
            const res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Login failed');

            this.setSession(data.access_token, data.user);
            UI.showSection('dashboard');
            Dashboard.load();
        } catch (err) {
            alert('Login failed: ' + err.message);
        }
    },

    async register(e) {
        e.preventDefault();
        const formData = {
            full_name: document.getElementById('regFullName').value.trim(),
            email: document.getElementById('regEmail').value.trim(),
            username: document.getElementById('regUsername').value.trim(),
            password: document.getElementById('regPassword').value,
            user_type: document.getElementById('regUserType').value,
            organization_name: document.getElementById('regOrgName').value.trim() || null
        };

        try {
            const res = await fetch(`${API_BASE}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Registration failed');
            }

            alert('Registration successful! Please log in.');
            document.querySelector('[data-tab="login"]').click();
        } catch (err) {
            alert('Error: ' + err.message);
        }
    },

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        UI.showSection('authSection');
    },

    setSession(token, user) {
        this.token = token;
        this.user = user;
        localStorage.setItem('authToken', token);
    },

    headers() {
        return {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json'
        };
    }
};

const UI = {
    showSection(id) {
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        document.getElementById(id)?.classList.add('active');

        // Highlight active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', link.dataset.section === id);
        });
    },

    initNav() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                UI.showSection(section);
                if (section !== 'authSection') window.history.pushState({}, '', `#${section}`);
            });
        });

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                document.getElementById('loginForm').classList.toggle('active', btn.dataset.tab === 'login');
                document.getElementById('registerForm').classList.toggle('active', btn.dataset.tab === 'register');
            });
        });
    }
};

const Dashboard = {
  {
  async load() {
        try {
            const [summaryRes, historyRes] = await Promise.all([
                fetch(`${API_BASE}/api/analytics/summary`, { headers: Auth.headers() }),
                fetch(`${API_BASE}/api/entries?limit=12`, { headers: Auth.headers() })
            ]);

            if (!summaryRes.ok || !historyRes.ok) throw new Error('Failed to load dashboard');

            const summary = await summaryRes.json();
            const entries = await historyRes.json();

            this.renderStats(summary);
            Charts.renderFootprint(entries.reverse());
        } catch (err) {
            document.getElementById('dashboardStats').innerHTML = '<p>Error loading dashboard.</p>';
        }
    },

    renderStats(data) {
        document.getElementById('latestFootprint').textContent = data.latest_footprint || '-';
        document.getElementById('avgFootprint').textContent = data.average_footprint || '-';
        document.getElementById('totalEntries').textContent = data.total_entries || '0';

        const trend = document.getElementById('trend');
        const label = document.getElementById('trendLabel');
        if (data.trend === 'decreasing') {
            trend.textContent = 'Down';
            label.textContent = 'Improving';
        } else if (data.trend === 'increasing') {
            trend.textContent = 'Up';
            label.textContent = 'Worsening';
        } else {
            trend.textContent = 'Right Arrow';
            label.textContent = 'Stable';
        }
    }
};

const Charts = {
    footprint: null,
    prediction: null,
    benchmark: null,

    renderFootprint(entries) {
        const ctx = document.getElementById('footprintChart');
        const labels = entries.map(e => new Date(e.entry_date).toLocaleDateString());
        const data = entries.map(e => e.total_carbon_footprint);

        if (this.footprint) this.footprint.destroy();
        this.footprint = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Carbon Footprint (kg CO₂)',
                    data,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { title: { display: true, text: 'Footprint Over Time' } },
                scales: { y: { beginAtZero: true } }
            }
        });
    }
    // Add prediction & benchmark charts similarly...
};

// Init on load
document.addEventListener('DOMContentLoaded', () => {
    UI.initNav();

    // Show org name field if not individual
    document.getElementById('regUserType').addEventListener('change', (e) => {
        document.getElementById('orgNameGroup').style.display = e.target.value === 'individual' ? 'none' : 'block';
    });

    // Check auth state
    if (Auth.token) {
        fetch(`${API_BASE}/api/auth/me`, { headers: Auth.headers() })
            .then(r => r.ok ? r.json() : Promise.reject())
            .then(user => {
                Auth.user = user;
                UI.showSection('dashboard');
                Dashboard.load();
                // Show corporate fields if needed
                if (user.user_type !== 'individual') {
                    document.getElementById('corporateSection').style.display = 'block';
                }
            })
            .catch(() => {
                Auth.logout();
            });
    }

    // Form submit
    document.getElementById('calculateForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = Object.fromEntries(new FormData(e.target));

        // Convert empty strings to 0
        Object.keys(formData).forEach(k => {
            if (formData[k] === '' || isNaN(formData[k])) && (formData[k] = 0);
        });

        try {
            const res = await fetch(`${API_BASE}/api/calculate`, {
                method: 'POST',
                headers: Auth.headers(),
                body: JSON.stringify(formData)
            });

            const result = await res.json();
            if (!res.ok) throw new Error(result.detail || 'Calculation failed');

            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsContent').innerHTML = renderResults(result);
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });

            Dashboard.load(); // Refresh
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });
});

function renderResults(data) {
    const f = data.footprint;
    return `
    <div class="total-footprint">
      <div class="label">Total Impact</div>
      <div class="value">${f.total.toLocaleString()} kg CO₂e</div>
      ${f.per_person ? `<div>Per Person: ${f.per_person.toFixed(1)} kg</div>` : ''}
    </div>
    <h4>Breakdown</h4>
    <div class="footprint-breakdown">
      ${Object.entries(f).filter(([k]) => !['total', 'per_person'].includes(k)).map(([k, v]) => `
        <div><strong>${k.charAt(0).toUpperCase() + k.slice(1)}:</strong> ${v} kg</div>
      `).join('')}
    </div>
  `;
}