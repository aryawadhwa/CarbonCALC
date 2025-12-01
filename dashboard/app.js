// app.js - Clean, modular, and maintainable
const API_BASE = window.location.origin;

const Auth = {
    token: localStorage.getItem('authToken'),
    user: null,

    async initDemo() {
        console.log('Initializing Demo Mode...');
        // Check if we already have a token, if not, try to login as demo user
        if (!this.token) {
            await this.loginDemo();
        } else {
            // Verify token is valid
            try {
                const res = await fetch(`${API_BASE}/api/auth/me`, { headers: this.headers() });
                if (!res.ok) throw new Error('Token invalid');
                this.user = await res.json();
                this.startApp();
            } catch (e) {
                await this.loginDemo();
            }
        }
    },

    async loginDemo() {
        console.log('Attempting Demo Login...');
        const demoCreds = { username: 'demo_factory', password: 'demo_password' };

        try {
            // Try login first
            let res = await fetch(`${API_BASE}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(demoCreds)
            });

            // If login fails (likely user doesn't exist), register then login
            if (!res.ok) {
                console.log('Demo user not found, registering...');
                const regRes = await fetch(`${API_BASE}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        ...demoCreds,
                        full_name: 'Demo Factory',
                        email: 'demo@factory.com',
                        user_type: 'institution',
                        organization_name: 'GreenFuture Manufacturing'
                    })
                });

                if (!regRes.ok) {
                    console.warn('Registration failed, falling back to mock mode immediately.');
                    this.mockSession();
                    return;
                }

                // Retry login
                res = await fetch(`${API_BASE}/api/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(demoCreds)
                });
            }

            if (res.ok) {
                const data = await res.json();
                this.setSession(data.access_token, data.user);
                this.startApp();
            } else {
                console.warn('Login failed after registration, using mock session.');
                this.mockSession();
            }
        } catch (err) {
            console.error('Demo login network error:', err);
            this.mockSession();
        }
    },

    mockSession() {
        console.log('Using Mock Session');
        this.user = {
            username: 'demo_factory',
            full_name: 'Demo Factory',
            email: 'demo@factory.com',
            user_type: 'institution',
            organization_name: 'GreenFuture Manufacturing'
        };
        this.token = 'mock_token';
        this.startApp();
    },

    startApp() {
        UI.showSection('dashboard');
        Dashboard.load();

        // Pre-fill form with factory data
        setTimeout(() => {
            const form = document.getElementById('calculateForm');
            if (form) {
                form.electricity_usage.value = 15000;
                form.gas_usage.value = 5000;
                form.heating_oil.value = 2000;
                form.vehicle_miles.value = 1200;
                form.waste_produced.value = 800;
                form.recycling_rate.value = 45;
                form.hazardous_waste.value = 150;
                form.employee_count.value = 150;
                form.office_space_sqm.value = 5000;
                // Trigger change events if needed
            }

            // Show corporate fields
            if (this.user.user_type !== 'individual') {
                document.getElementById('corporateSection')?.classList.remove('hidden');
            }
        }, 500);
    },

    async login(e) {
        // ... kept for manual override if needed, but UI is hidden
        e.preventDefault();
        // ...
    },

    // ... (keep register, logout, setSession, headers) ...

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('authToken');
        location.reload(); // Reload to re-trigger demo login
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
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active', 'block'));
        document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));

        const activeSection = document.getElementById(id);
        if (activeSection) {
            activeSection.classList.remove('hidden');
            activeSection.classList.add('active', 'block');
        }

        // Highlight active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('text-primary', link.dataset.section === id);
            link.classList.toggle('text-muted-foreground', link.dataset.section !== id);
        });

        // Load section data
        if (Sections[id]) Sections[id]();
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
                document.querySelectorAll('.tab-btn').forEach(b => {
                    b.classList.remove('active', 'bg-background', 'shadow-sm', 'text-foreground');
                    b.classList.add('text-muted-foreground', 'hover:text-foreground');
                });
                btn.classList.add('active', 'bg-background', 'shadow-sm', 'text-foreground');
                btn.classList.remove('text-muted-foreground', 'hover:text-foreground');

                document.getElementById('loginForm').classList.toggle('active', btn.dataset.tab === 'login');
                document.getElementById('loginForm').classList.toggle('hidden', btn.dataset.tab !== 'login');

                document.getElementById('registerForm').classList.toggle('active', btn.dataset.tab === 'register');
                document.getElementById('registerForm').classList.toggle('hidden', btn.dataset.tab !== 'register');
            });
        });
    }
};

const Sections = {
    async dashboard() {
        Dashboard.load();
    },

    async recommendations() {
        try {
            const res = await fetch(`${API_BASE}/api/recommendations`, { headers: Auth.headers() });
            const data = await res.json();

            const container = document.getElementById('recommendations');
            if (!res.ok) {
                container.innerHTML = '<div class="text-center py-12 text-muted-foreground">Failed to load recommendations.</div>';
                return;
            }

            container.innerHTML = `
                <div class="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background p-8">
                    <div class="max-w-5xl mx-auto">
                        <div class="mb-8 animate-slide-up">
                            <div class="flex items-center gap-3 mb-3">
                                <div class="p-2 rounded-lg bg-primary/10">
                                    <i data-lucide="lightbulb" class="w-6 h-6 text-primary"></i>
                                </div>
                                <h1 class="text-4xl md:text-5xl font-display font-bold text-foreground">Recommendations</h1>
                            </div>
                            <p class="text-lg text-muted-foreground">Biosafety & mitigation strategies tailored for your organization</p>
                        </div>
                        <div class="space-y-6">
                            ${data.length ? data.map((rec, idx) => `
                                <div class="animate-slide-up border border-border/50 bg-card/80 backdrop-blur-sm rounded-xl p-6 hover:shadow-lg transition-all duration-300" style="animation-delay: ${idx * 100}ms">
                                    <div class="flex items-start justify-between gap-4">
                                        <div class="flex-1">
                                            <div class="flex items-center gap-2 mb-2">
                                                <span class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80">
                                                    ${rec.category || 'General'}
                                                </span>
                                                <span class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent ${rec.impact_rating >= 4 ? 'bg-destructive/10 text-destructive' : 'bg-secondary/10 text-secondary-foreground'}">
                                                    ${rec.impact_rating >= 4 ? 'High' : 'Medium'} Priority
                                                </span>
                                            </div>
                                            <h3 class="text-xl font-display font-semibold mb-1">${rec.title}</h3>
                                            <p class="text-base text-muted-foreground">${rec.description}</p>
                                        </div>
                                        <div class="text-right">
                                            <div class="text-2xl font-bold text-primary">-${rec.estimated_reduction} kg</div>
                                            <div class="text-xs text-muted-foreground">potential impact</div>
                                        </div>
                                    </div>
                                    <div class="mt-4">
                                        <button class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-9 px-4 py-2 gap-2">
                                            Learn More <i data-lucide="arrow-right" class="w-4 h-4"></i>
                                        </button>
                                    </div>
                                </div>
                            `).join('') : '<div class="text-center text-muted-foreground">No recommendations found.</div>'}
                        </div>
                    </div>
                </div>
            `;
            lucide.createIcons();
        } catch (err) {
            console.error(err);
        }
    },

    async benchmarks() {
        try {
            const res = await fetch(`${API_BASE}/api/benchmark/compare`, { headers: Auth.headers() });
            const data = await res.json();
            if (res.ok) {
                const container = document.getElementById('benchmarks');
                container.innerHTML = `
                    <div class="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background p-8">
                        <div class="max-w-7xl mx-auto">
                            <div class="mb-8 animate-slide-up">
                                <div class="flex items-center gap-3 mb-3">
                                    <div class="p-2 rounded-lg bg-primary/10">
                                        <i data-lucide="bar-chart-3" class="w-6 h-6 text-primary"></i>
                                    </div>
                                    <h1 class="text-4xl md:text-5xl font-display font-bold text-foreground">Industry Benchmarks</h1>
                                </div>
                                <p class="text-lg text-muted-foreground">Compare your performance against industry standards</p>
                            </div>
                            <div class="animate-slide-up border border-border/50 bg-card/80 backdrop-blur-sm rounded-xl overflow-hidden">
                                <div class="p-6 border-b border-border/50">
                                    <h3 class="text-2xl font-display font-semibold">Benchmark Comparison</h3>
                                    <p class="text-sm text-muted-foreground">Your organization vs. industry average</p>
                                </div>
                                <div class="p-6">
                                    <div class="h-96 w-full relative">
                                        <canvas id="benchmarkChart"></canvas>
                                    </div>
                                    <div id="benchmarkStats" class="mt-8"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                lucide.createIcons();
                Charts.renderBenchmark(data);
            }
        } catch (err) { console.error(err); }
    },

    async predictions() {
        try {
            const res = await fetch(`${API_BASE}/api/predict?forecast_periods=12`, {
                method: 'POST',
                headers: Auth.headers()
            });
            const data = await res.json();
            if (res.ok) {
                Charts.renderPrediction(data);
                document.getElementById('predictionStats').innerHTML = `
                    <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                        <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Projected Annual</div>
                        <div class="text-3xl font-bold text-primary mt-2">${Math.round(data.projected_annual).toLocaleString()} <span class="text-sm font-normal text-muted-foreground">kg</span></div>
                    </div>
                    <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                        <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Trend</div>
                        <div class="text-3xl font-bold mt-2 capitalize ${data.trend_analysis.trend === 'decreasing' ? 'text-primary' : 'text-destructive'}">${data.trend_analysis.trend}</div>
                    </div>
                    <div class="p-6 rounded-xl border bg-card text-card-foreground shadow-sm">
                        <div class="text-sm font-medium text-muted-foreground uppercase tracking-wider">Reduction Potential</div>
                        <div class="text-3xl font-bold text-primary mt-2">${Math.round(data.trend_analysis.projected_reduction_potential).toLocaleString()} <span class="text-sm font-normal text-muted-foreground">kg</span></div>
                    </div>
                `;
            }
        } catch (err) { console.error(err); }
    },

    async history() {
        try {
            const res = await fetch(`${API_BASE}/api/entries?limit=20`, { headers: Auth.headers() });
            const entries = await res.json();

            const container = document.getElementById('historyContent');
            if (entries.length === 0) {
                container.innerHTML = '<div class="text-center py-12 text-muted-foreground">No history available.</div>';
                return;
            }

            container.innerHTML = entries.map(entry => `
                <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between p-6 rounded-xl border bg-card text-card-foreground shadow-sm hover:bg-muted/50 transition-colors gap-4">
                    <div>
                        <div class="text-sm text-muted-foreground mb-1">${new Date(entry.entry_date).toLocaleDateString(undefined, { dateStyle: 'full' })}</div>
                        <div class="font-bold text-2xl text-foreground">${entry.total_carbon_footprint.toLocaleString()} <span class="text-sm font-normal text-muted-foreground">kg CO₂</span></div>
                    </div>
                    <div class="flex gap-2 flex-wrap">
                        ${Object.entries(entry.category_breakdown || {}).filter(([k]) => !['total', 'per_person'].includes(k)).slice(0, 3).map(([k, v]) => `
                            <span class="inline-flex items-center rounded-md bg-muted px-2 py-1 text-xs font-medium ring-1 ring-inset ring-gray-500/10 capitalize">
                                ${k}: ${Math.round(v)}
                            </span>
                        `).join('')}
                    </div>
                </div>
            `).join('');
        } catch (err) { console.error(err); }
    },

    async profile() {
        if (!Auth.user) await fetch(`${API_BASE}/api/auth/me`, { headers: Auth.headers() }).then(r => r.json()).then(u => Auth.user = u);
        const u = Auth.user;

        // Ensure profile section exists or target it correctly
        // Assuming profile section structure is still there
        const container = document.getElementById('profile');
        // We can just inject into a specific container if we didn't wipe the section content.
        // But for consistency, let's assume we might want to style it too.
        // For now, I'll just update the inner content if I can find the container.
        // The original HTML has <section id="profile"> ... </section>
        // I didn't wipe it.
        // So I should target a container inside it if I want to keep the header.
        // But wait, the original code targeted `profileContent`?
        // Let's check the original code in Step 239 replacement.
        // It targeted `document.getElementById('profileContent')`.
        // Does `profileContent` exist in index.html?
        // Step 272 shows `section id="profile" ... <h2 ...>Profile Settings</h2>`.
        // It does NOT show `profileContent` div.
        // I should probably add it or target the section and rebuild it.

        container.innerHTML = `
            <div class="container mx-auto px-4 py-8 max-w-2xl">
                <h2 class="text-3xl font-bold tracking-tight mb-8">Profile Settings</h2>
                <div class="grid gap-6 md:grid-cols-2">
                    <div class="space-y-2">
                        <label class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">Full Name</label>
                        <div class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-muted-foreground">${u.full_name}</div>
                    </div>
                    <div class="space-y-2">
                        <label class="text-sm font-medium leading-none">Email</label>
                        <div class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-muted-foreground">${u.email}</div>
                    </div>
                    <div class="space-y-2">
                        <label class="text-sm font-medium leading-none">Username</label>
                        <div class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-muted-foreground">${u.username}</div>
                    </div>
                    <div class="space-y-2">
                        <label class="text-sm font-medium leading-none">Entity Type</label>
                        <div class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-muted-foreground capitalize">${u.user_type}</div>
                    </div>
                    ${u.organization_name ? `
                    <div class="space-y-2 md:col-span-2">
                        <label class="text-sm font-medium leading-none">Organization</label>
                        <div class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm text-muted-foreground">${u.organization_name}</div>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
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
    },
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

    // Initialize Demo Mode (Auto-login)
    Auth.initDemo();

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