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
        const statsHtml = `
            <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Latest Impact</div>
                <div class="text-3xl font-bold text-primary mt-2">${data.latest_footprint || '-'} <span class="text-sm font-normal text-muted-foreground">kg CO₂</span></div>
            </div>
            <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Average</div>
                <div class="text-3xl font-bold text-primary mt-2">${data.average_footprint || '-'} <span class="text-sm font-normal text-muted-foreground">kg CO₂</span></div>
            </div>
            <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Total Entries</div>
                <div class="text-3xl font-bold text-primary mt-2">${data.total_entries || '0'}</div>
            </div>
            <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Trend</div>
                <div class="text-3xl font-bold mt-2 ${data.trend === 'decreasing' ? 'text-primary' : data.trend === 'increasing' ? 'text-destructive' : 'text-muted-foreground'}">
                    ${data.trend === 'decreasing' ? '↓ Improving' : data.trend === 'increasing' ? '↑ Worsening' : '→ Stable'}
                </div>
            </div>
        `;
        document.getElementById('dashboardStats').innerHTML = statsHtml;
    }
};

const Charts = {
    footprint: null,
    prediction: null,
    benchmark: null,

    renderFootprint(entries) {
        const ctx = document.getElementById('footprintChart');
        const labels = entries.map(e => new Date(e.entry_date).toISOString());
        const data = entries.map(e => e.total_carbon_footprint);

        if (this.footprint) this.footprint.destroy();
        this.footprint = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Carbon Footprint',
                    data,
                    borderColor: 'hsl(155, 65%, 25%)',
                    backgroundColor: 'hsla(155, 65%, 25%, 0.1)',
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: 'hsl(155, 65%, 25%)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'hsl(var(--popover))',
                        titleColor: 'hsl(var(--popover-foreground))',
                        bodyColor: 'hsl(var(--popover-foreground))',
                        borderColor: 'hsl(var(--border))',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: false
                    }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: { unit: 'day' },
                        grid: { display: false },
                        ticks: { color: 'hsl(var(--muted-foreground))' }
                    },
                    y: {
                        beginAtZero: true,
                        grid: { color: 'hsl(var(--border))', borderDash: [4, 4] },
                        ticks: { color: 'hsl(var(--muted-foreground))' }
                    }
                }
            }
        });
    }
    renderPrediction(data) {
        const ctx = document.getElementById('predictionChart');
        if (!ctx) return;
        if (this.prediction) this.prediction.destroy();

        const predictions = data.predictions;
        const intervals = data.confidence_intervals;
        const labels = Array.from({ length: predictions.length }, (_, i) => `Month ${i + 1}`);

        this.prediction = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: 'Forecast',
                        data: predictions,
                        borderColor: 'hsl(var(--primary))',
                        backgroundColor: 'hsl(var(--primary) / 0.1)',
                        tension: 0.4,
                        fill: false,
                        pointBackgroundColor: 'hsl(var(--primary))',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    },
                    {
                        label: 'Upper Bound',
                        data: intervals.map(i => i.upper),
                        borderColor: 'hsl(var(--primary) / 0.2)',
                        backgroundColor: 'hsl(var(--primary) / 0.1)',
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: '+1'
                    },
                    {
                        label: 'Lower Bound',
                        data: intervals.map(i => i.lower),
                        borderColor: 'hsl(var(--primary) / 0.2)',
                        backgroundColor: 'transparent',
                        borderDash: [5, 5],
                        pointRadius: 0,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, labels: { color: 'hsl(var(--muted-foreground))' } },
                    tooltip: {
                        backgroundColor: 'hsl(var(--popover))',
                        titleColor: 'hsl(var(--popover-foreground))',
                        bodyColor: 'hsl(var(--popover-foreground))',
                        borderColor: 'hsl(var(--border))',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: { grid: { display: false }, ticks: { color: 'hsl(var(--muted-foreground))' } },
                    y: { grid: { color: 'hsl(var(--border))', borderDash: [4, 4] }, ticks: { color: 'hsl(var(--muted-foreground))' } }
                }
            }
        });
    },

    renderBenchmark(data) {
        const ctx = document.getElementById('benchmarkChart');
        if (!ctx) return;
        if (this.benchmark) this.benchmark.destroy();

        this.benchmark = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Your Impact', 'Industry Avg', 'Top Performers'],
                datasets: [{
                    label: 'Carbon Footprint (kg CO₂)',
                    data: [
                        data.user_footprint,
                        data.benchmark.average_carbon_total,
                        data.benchmark.average_carbon_total * 0.75
                    ],
                    backgroundColor: [
                        'hsl(var(--primary))',
                        'hsl(var(--muted))',
                        'hsl(var(--secondary))'
                    ],
                    borderRadius: 6,
                    barThickness: 40
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'hsl(var(--popover))',
                        titleColor: 'hsl(var(--popover-foreground))',
                        bodyColor: 'hsl(var(--popover-foreground))',
                        borderColor: 'hsl(var(--border))',
                        borderWidth: 1,
                        padding: 12,
                        cornerRadius: 8
                    }
                },
                scales: {
                    x: { grid: { display: false }, ticks: { color: 'hsl(var(--muted-foreground))' } },
                    y: { grid: { color: 'hsl(var(--border))', borderDash: [4, 4] }, ticks: { color: 'hsl(var(--muted-foreground))' } }
                }
            }
        });
    }
};

// Init on load
document.addEventListener('DOMContentLoaded', () => {
    UI.initNav();

    // Show org name field if not individual
    document.getElementById('regUserType').addEventListener('change', (e) => {
        const orgGroup = document.getElementById('orgNameGroup');
        orgGroup.classList.toggle('hidden', e.target.value === 'individual');
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
                    document.getElementById('corporateSection').classList.remove('hidden');
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
            if ((formData[k] === '' || !isNaN(formData[k])) && k !== 'notes') {
                formData[k] = parseFloat(formData[k]) || 0;
            }
        });

        try {
            const res = await fetch(`${API_BASE}/api/calculate`, {
                method: 'POST',
                headers: Auth.headers(),
                body: JSON.stringify(formData)
            });

            const result = await res.json();
            if (!res.ok) throw new Error(result.detail || 'Calculation failed');

            const resultsSection = document.getElementById('resultsSection');
            resultsSection.classList.remove('hidden');
            document.getElementById('resultsContent').innerHTML = renderResults(result);
            resultsSection.scrollIntoView({ behavior: 'smooth' });

            Dashboard.load(); // Refresh
        } catch (err) {
            alert('Error: ' + err.message);
        }
    });
});

function renderResults(data) {
    const f = data.footprint;
    return `
    <div class="text-center p-8 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20 mb-8">
      <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-2">Total Impact</div>
      <div class="text-5xl font-bold text-primary mb-2">${f.total.toLocaleString()} <span class="text-2xl text-muted-foreground font-normal">kg CO₂e</span></div>
      ${f.per_person ? `<div class="text-sm text-muted-foreground">Per Person: <span class="font-medium text-foreground">${f.per_person.toFixed(1)} kg</span></div>` : ''}
    </div>
    
    <h4 class="text-lg font-semibold mb-4">Emissions Breakdown</h4>
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      ${Object.entries(f).filter(([k]) => !['total', 'per_person'].includes(k)).map(([k, v]) => `
        <div class="p-4 rounded-lg bg-muted/50 border border-border flex items-center justify-between">
            <span class="text-sm font-medium capitalize text-muted-foreground">${k}</span>
            <span class="text-lg font-bold text-foreground">${v} <span class="text-xs font-normal text-muted-foreground">kg</span></span>
        </div>
      `).join('')}
    </div>
  `;
}