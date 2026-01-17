// SDG Digital Twin Platform - Frontend Application
// API Configuration
const API_BASE = 'http://localhost:8000';

// Global state
let currentTwin = null;
let currentScenario = 'success';
let selectedSDGs = [];
let allSDGs = {};
let digitalTwins = [];
let organizations = [];
let projects = [];

// Initialize app (only runs on index.html - old structure)
// Individual pages load their own data via page-specific scripts
if (document.getElementById('simulate-section')) {
    // Old index.html structure
    document.addEventListener('DOMContentLoaded', async () => {
        console.log('🚀 SDG Digital Twin Platform Initialized');
        
        // Check authentication and update nav
        updateNavigationAuth();
        
        // Setup navigation
        setupNavigation();
        
        // Setup slider listeners
        setupSliders();
        
    // Setup scenario buttons
        setupScenarioButtons();
        
        // Load initial data
        await loadSDGs();
        await loadDigitalTwins();
        await loadOrganizations();
        await loadProjects();
        
        // Setup SDG selectors
        setupSDGSelectors();
    });
}

// Update navigation based on auth status
function updateNavigationAuth() {
    const isLoggedIn = isAuthenticated();
    const navUser = document.getElementById('navUser');
    const navAuth = document.getElementById('navAuth');
    
    if (isLoggedIn) {
        if (navUser) navUser.style.display = 'flex';
        if (navAuth) navAuth.style.display = 'none';
    } else {
        if (navUser) navUser.style.display = 'none';
        if (navAuth) navAuth.style.display = 'flex';
    }
}

// Navigation
function setupNavigation() {
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const section = btn.dataset.section;
            
            // Update active nav button
            document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // Show corresponding section
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById(`${section}-section`).classList.add('active');
        });
    });
}

// Setup sliders with real-time updates
function setupSliders() {
    const fundingSlider = document.getElementById('funding-slider');
    const timelineSlider = document.getElementById('timeline-slider');
    const delaySlider = document.getElementById('delay-slider');
    
    fundingSlider.addEventListener('input', (e) => {
        document.getElementById('funding-value').textContent = e.target.value;
    });
    
    timelineSlider.addEventListener('input', (e) => {
        document.getElementById('timeline-value').textContent = e.target.value;
    });
    
    delaySlider.addEventListener('input', (e) => {
        document.getElementById('delay-value').textContent = e.target.value;
    });
}

// Setup scenario buttons
function setupScenarioButtons() {
    document.querySelectorAll('.scenario-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentScenario = btn.dataset.scenario;
        });
    });
}

// Load SDGs
async function loadSDGs() {
    try {
        const response = await fetch(`${API_BASE}/sdgs`);
        const data = await response.json();
        allSDGs = data;
        console.log('✅ Loaded 17 SDGs');
    } catch (error) {
        console.error('Error loading SDGs:', error);
    }
}

// Load Digital Twins
async function loadDigitalTwins() {
    try {
        const response = await fetch(`${API_BASE}/digital-twins`);
        digitalTwins = await response.json();
        renderDigitalTwins();
        updateTwinSelectors();
        console.log(`✅ Loaded ${digitalTwins.length} Digital Twins`);
    } catch (error) {
        console.error('Error loading digital twins:', error);
    }
}

// Render Digital Twins
function renderDigitalTwins() {
    const grid = document.getElementById('twins-grid');
    if (!grid) return; // Element doesn't exist on this page
    
    if (digitalTwins.length === 0) {
        grid.innerHTML = '<p style="color: #64748b;">No digital twins yet. Create your first one!</p>';
        return;
    }
    
    grid.innerHTML = digitalTwins.map(twin => `
        <div class="twin-card fade-in" onclick="selectTwinForSimulation(${twin.id})">
            <h3>${twin.name}</h3>
            <p style="color: #64748b; font-size: 14px; margin: 8px 0;">
                ${twin.region}, ${twin.country}
            </p>
            <p style="font-size: 13px; color: #475569;">
                ${twin.description || 'Digital twin ready for simulation'}
            </p>
            <div class="twin-meta">
                <span>👥 ${twin.population.toLocaleString()}</span>
                <span>📍 ${twin.area_km2} km²</span>
                <span>📅 ${twin.baseline_year}</span>
            </div>
        </div>
    `).join('');
}

// Update twin selectors
function updateTwinSelectors() {
    const simSelect = document.getElementById('sim-twin-select');
    const projectSelect = document.getElementById('project-twin-select');
    
    const options = digitalTwins.map(t => 
        `<option value="${t.id}">${t.name} (${t.region})</option>`
    ).join('');
    
    if (simSelect) {
        simSelect.innerHTML = '<option value="">Choose a digital twin...</option>' + options;
    }
    if (projectSelect) {
        projectSelect.innerHTML = '<option value="">None</option>' + options;
    }
}

// Setup SDG Selectors
function setupSDGSelectors() {
    const mainSelector = document.getElementById('sdg-selector');
    const orgSelector = document.getElementById('org-sdg-selector');
    const projectSelector = document.getElementById('project-sdg-selector');
    
    if (!allSDGs.goals) return;
    
    // Main simulation selector (with grid layout)
    mainSelector.innerHTML = Object.entries(allSDGs.goals).map(([num, name]) => `
        <div class="sdg-chip" data-sdg="${num}" onclick="toggleSDG(${num})">
            SDG ${num}
        </div>
    `).join('');
    
    // Compact selectors for modals
    const compactHTML = Object.entries(allSDGs.goals).map(([num, name]) => `
        <div class="sdg-chip" data-sdg="${num}" onclick="toggleSDGCompact(this, ${num})">
            ${num}
        </div>
    `).join('');
    
    orgSelector.innerHTML = compactHTML;
    projectSelector.innerHTML = compactHTML;
}

// Toggle SDG selection
function toggleSDG(sdgNum) {
    const chip = document.querySelector(`#sdg-selector .sdg-chip[data-sdg="${sdgNum}"]`);
    chip.classList.toggle('selected');
    
    if (selectedSDGs.includes(sdgNum)) {
        selectedSDGs = selectedSDGs.filter(s => s !== sdgNum);
    } else {
        selectedSDGs.push(sdgNum);
    }
}

// Toggle SDG for compact selectors
function toggleSDGCompact(element, sdgNum) {
    element.classList.toggle('selected');
}

// Get selected SDGs from compact selector
function getSelectedSDGsCompact(selectorId) {
    const selected = [];
    document.querySelectorAll(`#${selectorId} .sdg-chip.selected`).forEach(chip => {
        selected.push(parseInt(chip.dataset.sdg));
    });
    return selected;
}

// Select twin for simulation
function selectTwinForSimulation(twinId) {
    document.getElementById('sim-twin-select').value = twinId;
    loadTwinForSimulation();
    
    // Switch to simulation tab
    document.querySelector('.nav-btn[data-section="simulate"]').click();
}

// Load twin for simulation
async function loadTwinForSimulation() {
    const twinId = document.getElementById('sim-twin-select').value;
    if (!twinId) {
        currentTwin = null;
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/digital-twins/${twinId}`);
        currentTwin = await response.json();
        console.log('✅ Loaded twin for simulation:', currentTwin.twin.name);
    } catch (error) {
        console.error('Error loading twin:', error);
    }
}

// Run Simulation (CORE FEATURE)
async function runSimulation() {
    if (!currentTwin) {
        alert('Please select a Digital Twin first');
        return;
    }
    
    if (selectedSDGs.length === 0) {
        alert('Please select at least one target SDG');
        return;
    }
    
    const funding = parseFloat(document.getElementById('funding-slider').value);
    const timeline = parseInt(document.getElementById('timeline-slider').value);
    const delay = parseInt(document.getElementById('delay-slider').value);
    const projectId = document.getElementById('sim-project-select').value || null;
    
    // Show loading
    const output = document.getElementById('simulation-output');
    output.innerHTML = '<div style="text-align: center; padding: 100px;"><div class="loading"></div><p>Simulating future impact...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/simulations/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                digital_twin_id: currentTwin.twin.id,
                project_id: projectId,
                scenario_type: currentScenario,
                simulation_name: `${currentScenario.replace('_', ' ').toUpperCase()} Scenario`,
                target_sdgs: selectedSDGs,
                funding_percentage: funding,
                timeline_years: timeline,
                delay_months: delay,
                scale_factor: 1.0
            })
        });
        
        const result = await response.json();
        console.log('🎯 Simulation complete:', result);
        
        // Display results
        displaySimulationResults(result);
        
    } catch (error) {
        console.error('Error running simulation:', error);
        output.innerHTML = '<div style="text-align: center; padding: 100px; color: #ef4444;"><h3>Simulation Error</h3><p>Failed to run simulation. Please try again.</p></div>';
    }
}

// Display Simulation Results with Charts
function displaySimulationResults(result) {
    const output = document.getElementById('simulation-output');
    
    // Sort outcomes by primary vs secondary
    const outcomes = result.predicted_outcomes;
    const primarySDGs = Object.entries(outcomes).filter(([_, data]) => !data.is_secondary);
    const secondarySDGs = Object.entries(outcomes).filter(([_, data]) => data.is_secondary);
    
    // Build results HTML
    let html = `
        <div class="results-header fade-in">
            <h3>🔮 ${result.simulation_name}</h3>
            <p>${currentTwin.twin.name} - ${result.timeline_years} Year Projection</p>
            <div class="results-stats">
                <div class="stat-box">
                    <span class="stat-value">${result.confidence_score * 100}%</span>
                    <span class="stat-label">Confidence</span>
                </div>
                <div class="stat-box">
                    <span class="stat-value">${result.affected_population.toLocaleString()}</span>
                    <span class="stat-label">People Affected</span>
                </div>
                <div class="stat-box">
                    <span class="stat-value">${Object.keys(outcomes).length}</span>
                    <span class="stat-label">SDGs Impacted</span>
                </div>
            </div>
        </div>
        
        <div class="explanation-box fade-in">
            <h4>📝 Impact Explanation</h4>
            <p>${result.explanation}</p>
        </div>
        
        <div class="explanation-box policy-insight fade-in">
            <h4>💡 Policy Insight</h4>
            <p>${result.policy_insight}</p>
        </div>
    `;
    
    if (result.risk_warning) {
        html += `
            <div class="explanation-box risk-warning fade-in">
                <h4>⚠️ Risk Warning</h4>
                <p>${result.risk_warning}</p>
            </div>
        `;
    }
    
    html += '<h4 style="margin: 24px 0 16px; color: #2563eb;">Primary SDG Impacts</h4><div class="sdg-impacts">';
    
    // Render primary SDG impacts with charts
    primarySDGs.forEach(([sdgNum, data]) => {
        const isPositive = data.change > 0;
        const changePercent = ((data.change / data.baseline) * 100).toFixed(1);
        
        html += `
            <div class="sdg-impact-card ${isPositive ? 'positive' : 'negative'} fade-in">
                <div class="sdg-impact-header">
                    <h4>SDG ${sdgNum}: ${data.sdg_name}</h4>
                    <span class="change-badge ${isPositive ? 'positive' : 'negative'}">
                        ${isPositive ? '↑' : '↓'} ${Math.abs(data.change).toFixed(1)} ${data.unit}
                        (${changePercent}%)
                    </span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; color: #64748b;">
                    <span>Baseline: ${data.baseline} ${data.unit}</span>
                    <span>Final: ${data.final} ${data.unit}</span>
                </div>
                <canvas id="chart-${sdgNum}" class="timeline-chart"></canvas>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Secondary impacts
    if (secondarySDGs.length > 0) {
        html += '<h4 style="margin: 24px 0 16px; color: #10b981;">Secondary SDG Effects (Ripple Impact)</h4><div class="sdg-impacts">';
        
        secondarySDGs.forEach(([sdgNum, data]) => {
            const isPositive = data.change > 0;
            html += `
                <div class="sdg-impact-card ${isPositive ? 'positive' : 'negative'} fade-in" style="opacity: 0.8;">
                    <div class="sdg-impact-header">
                        <h4>SDG ${sdgNum}: ${data.sdg_name}</h4>
                        <span class="change-badge ${isPositive ? 'positive' : 'negative'}">
                            ${isPositive ? '↑' : '↓'} ${Math.abs(data.change).toFixed(1)} ${data.unit}
                        </span>
                    </div>
                    <p style="font-size: 13px; color: #64748b;">Cross-SDG influence effect</p>
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    output.innerHTML = html;
    
    // Render charts
    setTimeout(() => {
        primarySDGs.forEach(([sdgNum, data]) => {
            if (data.timeline) {
                renderTimelineChart(`chart-${sdgNum}`, data);
            }
        });
    }, 100);
}

// Render timeline chart
function renderTimelineChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const years = data.timeline.map(t => `Year ${t.year}`);
    const values = data.timeline.map(t => t.value);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: years,
            datasets: [{
                label: data.sdg_name,
                data: values,
                borderColor: data.change > 0 ? '#10b981' : '#ef4444',
                backgroundColor: data.change > 0 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                borderWidth: 3,
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (context) => `${context.parsed.y.toFixed(2)} ${data.unit}`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: (value) => `${value.toFixed(1)} ${data.unit}`
                    }
                }
            }
        }
    });
}

// Compare Scenarios
async function compareScenarios() {
    if (!currentTwin) {
        alert('Please select a Digital Twin first');
        return;
    }
    
    if (selectedSDGs.length === 0) {
        alert('Please select at least one target SDG');
        return;
    }
    
    const funding = parseFloat(document.getElementById('funding-slider').value);
    const timeline = parseInt(document.getElementById('timeline-slider').value);
    
    const output = document.getElementById('simulation-output');
    output.innerHTML = '<div style="text-align: center; padding: 100px;"><div class="loading"></div><p>Comparing all scenarios...</p></div>';
    
    try {
        const response = await fetch(`${API_BASE}/simulations/compare`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                digital_twin_id: currentTwin.twin.id,
                target_sdgs: selectedSDGs,
                scenarios: ['success', 'partial_success', 'delay', 'failure', 'underfunded'],
                funding_percentage: funding,
                timeline_years: timeline
            })
        });
        
        const results = await response.json();
        displayComparisonResults(results, timeline);
        
    } catch (error) {
        console.error('Error comparing scenarios:', error);
    }
}

// Display comparison results
function displayComparisonResults(results, timeline) {
    const output = document.getElementById('simulation-output');
    
    let html = `
        <div class="results-header fade-in">
            <h3>📊 Scenario Comparison</h3>
            <p>${currentTwin.twin.name} - ${timeline} Year Projections</p>
        </div>
        
        <div class="comparison-grid">
    `;
    
    const scenarioNames = {
        'success': '✅ Success',
        'partial_success': '⚠️ Partial Success',
        'delay': '⏱️ Delayed',
        'failure': '❌ Failure',
        'underfunded': '💰 Underfunded'
    };
    
    Object.entries(results).forEach(([scenario, data]) => {
        const primaryOutcomes = Object.entries(data.outcomes).filter(([_, d]) => !d.is_secondary);
        const avgChange = primaryOutcomes.reduce((sum, [_, d]) => sum + d.change, 0) / primaryOutcomes.length;
        
        html += `
            <div class="comparison-card fade-in">
                <h4>${scenarioNames[scenario]}</h4>
                <div style="margin: 12px 0;">
                    <div class="stat-box" style="background: #f1f5f9; margin-bottom: 8px;">
                        <span class="stat-value" style="font-size: 20px; color: #1e293b;">
                            ${data.affected_population.toLocaleString()}
                        </span>
                        <span class="stat-label" style="color: #64748b;">People Affected</span>
                    </div>
                    <div class="stat-box" style="background: #f1f5f9;">
                        <span class="stat-value" style="font-size: 20px; color: ${avgChange > 0 ? '#10b981' : '#ef4444'};">
                            ${avgChange > 0 ? '↑' : '↓'} ${Math.abs(avgChange).toFixed(1)}
                        </span>
                        <span class="stat-label" style="color: #64748b;">Avg SDG Change</span>
                    </div>
                </div>
                <p style="font-size: 12px; color: #64748b; margin-top: 8px;">
                    Confidence: ${(data.confidence * 100).toFixed(0)}%
                </p>
            </div>
        `;
    });
    
    html += '</div>';
    
    output.innerHTML = html;
}

// Load Organizations
async function loadOrganizations() {
    try {
        const response = await fetch(`${API_BASE}/organizations`);
        organizations = await response.json();
        renderOrganizations();
        updateOrgSelectors();
        console.log(`✅ Loaded ${organizations.length} Organizations`);
    } catch (error) {
        console.error('Error loading organizations:', error);
    }
}

// Render Organizations
function renderOrganizations() {
    const grid = document.getElementById('orgs-grid');
    if (!grid) return; // Element doesn't exist on this page
    
    if (organizations.length === 0) {
        grid.innerHTML = '<p style="color: #64748b;">No organizations yet. Register your first one!</p>';
        return;
    }
    
    grid.innerHTML = organizations.map(org => `
        <div class="org-card fade-in">
            <h3>${org.name}</h3>
            <p style="color: #64748b; font-size: 14px; margin: 8px 0;">
                ${org.type}
            </p>
            <p style="font-size: 13px; color: #475569;">
                ${org.description || 'No description'}
            </p>
            <div class="org-sdgs">
                ${org.focus_sdgs.map(sdg => `<span class="sdg-badge">SDG ${sdg}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// Update org selectors
function updateOrgSelectors() {
    const select = document.getElementById('project-org-select');
    if (!select) return; // Element doesn't exist on this page
    
    select.innerHTML = '<option value="">Select organization...</option>' + 
        organizations.map(org => `<option value="${org.id}">${org.name}</option>`).join('');
}

// Load Projects
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/projects`);
        projects = await response.json();
        renderProjects();
        updateProjectSelectors();
        console.log(`✅ Loaded ${projects.length} Projects`);
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

// Render Projects
function renderProjects() {
    const grid = document.getElementById('projects-grid');
    if (!grid) return; // Element doesn't exist on this page
    
    if (projects.length === 0) {
        grid.innerHTML = '<p style="color: #64748b;">No projects yet. Create your first one!</p>';
        return;
    }
    
    grid.innerHTML = projects.map(project => `
        <div class="project-card fade-in">
            <h3>${project.title}</h3>
            <p style="font-size: 13px; color: #475569; margin: 8px 0;">
                ${project.description}
            </p>
            <div style="display: flex; gap: 16px; margin: 12px 0; font-size: 13px; color: #64748b;">
                <span>💰 $${project.budget.toLocaleString()}</span>
                <span>📅 ${project.timeline_months} months</span>
                <span>📊 ${project.status}</span>
            </div>
            <div class="project-sdgs">
                ${project.target_sdgs.map(sdg => `<span class="sdg-badge">SDG ${sdg}</span>`).join('')}
            </div>
        </div>
    `).join('');
}

// Update project selectors
function updateProjectSelectors() {
    const select = document.getElementById('sim-project-select');
    if (!select) return; // Element doesn't exist on this page
    
    select.innerHTML = '<option value="">No project / Custom simulation</option>' + 
        projects.map(p => `<option value="${p.id}">${p.title}</option>`).join('');
}

// Modal Functions
function showCreateTwinModal() {
    document.getElementById('create-twin-modal').classList.add('show');
}

function showCreateOrgModal() {
    document.getElementById('create-org-modal').classList.add('show');
}

function showCreateProjectModal() {
    document.getElementById('create-project-modal').classList.add('show');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('show');
}

// Create Digital Twin
async function createDigitalTwin(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    const data = {
        name: formData.get('name'),
        region: formData.get('region'),
        country: formData.get('country'),
        population: parseInt(formData.get('population')),
        area_km2: parseFloat(formData.get('area_km2')),
        description: formData.get('description'),
        region_type: formData.get('region_type')
    };
    
    console.log('Creating Digital Twin with data:', data);
    
    try {
        const response = await fetch(`${API_BASE}/digital-twins`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.text();
            console.error('API Error:', error);
            throw new Error(`HTTP ${response.status}: ${error}`);
        }
        
        const result = await response.json();
        console.log('✅ Created Digital Twin:', result);
        
        // Close modal and reset form
        closeModal('create-twin-modal');
        form.reset();
        
        // Reload twins to show the new one
        await loadDigitalTwins();
        
        alert(`✅ Digital Twin "${result.name}" created successfully!`);
    } catch (error) {
        console.error('Error creating digital twin:', error);
        alert(`Error creating digital twin: ${error.message}`);
    }
}

// Create Organization
async function createOrganization(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    const focusSDGs = getSelectedSDGsCompact('org-sdg-selector');
    
    const data = {
        name: formData.get('name'),
        type: formData.get('type'),
        description: formData.get('description'),
        focus_sdgs: focusSDGs
    };
    
    try {
        const response = await fetch(`${API_BASE}/organizations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('✅ Created Organization:', result);
        
        closeModal('create-org-modal');
        form.reset();
        document.querySelectorAll('#org-sdg-selector .sdg-chip').forEach(c => c.classList.remove('selected'));
        await loadOrganizations();
        
        alert('✅ Organization registered successfully!');
    } catch (error) {
        console.error('Error creating organization:', error);
        alert('Error registering organization. Please try again.');
    }
}

// Create Project
async function createProject(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    
    const targetSDGs = getSelectedSDGsCompact('project-sdg-selector');
    
    if (targetSDGs.length === 0) {
        alert('Please select at least one target SDG');
        return;
    }
    
    const twinId = formData.get('digital_twin_id');
    
    const data = {
        organization_id: parseInt(formData.get('organization_id')),
        digital_twin_id: twinId ? parseInt(twinId) : null,
        title: formData.get('title'),
        description: formData.get('description'),
        target_sdgs: targetSDGs,
        budget: parseFloat(formData.get('budget')),
        timeline_months: parseInt(formData.get('timeline_months')),
        status: 'Planning'
    };
    
    try {
        const response = await fetch(`${API_BASE}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        console.log('✅ Created Project:', result);
        
        closeModal('create-project-modal');
        form.reset();
        document.querySelectorAll('#project-sdg-selector .sdg-chip').forEach(c => c.classList.remove('selected'));
        await loadProjects();
        
        alert('✅ Project created successfully!');
    } catch (error) {
        console.error('Error creating project:', error);
        alert('Error creating project. Please try again.');
    }
}

// Close modals on background click
document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('show');
        }
    });
});
