# 🏗️ System Architecture

## **High-Level Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         USER BROWSER                         │
│                     (http://localhost:3000)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       FRONTEND LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  index.html  │  │  styles.css  │  │    app.js    │     │
│  │              │  │              │  │              │     │
│  │ • UI Layout  │  │ • Modern CSS │  │ • API Calls  │     │
│  │ • Modals     │  │ • Animations │  │ • Chart.js   │     │
│  │ • Forms      │  │ • Responsive │  │ • Real-time  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       BACKEND LAYER                          │
│                    (FastAPI on Port 8000)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                     main.py                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │  │
│  │  │  Digital   │  │ Simulation │  │    SDG     │    │  │
│  │  │    Twin    │  │  Endpoints │  │Collaboration│    │  │
│  │  │  Endpoints │  │            │  │ Endpoints  │    │  │
│  │  └────────────┘  └────────────┘  └────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            simulation_engine.py (CORE)                │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │         SimulationEngine Class              │    │  │
│  │  │  • simulate_future_impact()                 │    │  │
│  │  │  • calculate_secondary_impacts()            │    │  │
│  │  │  • compare_scenarios()                      │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │         AIExplainer Class                   │    │  │
│  │  │  • generate_explanation()                   │    │  │
│  │  │  • policy_insights()                        │    │  │
│  │  │  • risk_warnings()                          │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              database.py (ORM Models)                 │  │
│  │  • DigitalTwin    • SDGIndicator                      │  │
│  │  • Simulation     • Project                           │  │
│  │  • Organization   • Partnership                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           sdg_data.py (Reference Data)                │  │
│  │  • 17 SDG Definitions                                 │  │
│  │  • Key Indicators per SDG                             │  │
│  │  • Regional Baseline Templates                        │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SQLAlchemy ORM
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                         │
│                     (SQLite - sdg_platform.db)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │digital_twins │  │sdg_indicators│  │  simulations │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │organizations │  │   projects   │  │ partnerships │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## **Data Flow - Simulation Execution**

```
USER INTERACTION
      │
      ├─ Select Digital Twin
      ├─ Choose Target SDGs (e.g., 6, 11)
      ├─ Select Scenario (success/failure/delay/underfunded)
      ├─ Adjust Parameters (funding %, timeline, delay)
      │
      ▼
   FRONTEND
      │
      ├─ Validate inputs
      ├─ Build API request
      │
      ▼
   POST /simulations/run
      │
      ▼
   BACKEND API (main.py)
      │
      ├─ Fetch Digital Twin from DB
      ├─ Fetch SDG Indicators (baseline values)
      │
      ▼
   SIMULATION ENGINE
      │
      ├─ Calculate Impact Factor
      │   └─ scenario_multiplier × funding × delay × scale
      │
      ├─ Simulate Primary SDG Changes
      │   └─ Year-by-year progression (0 to N)
      │       └─ change = baseline × growth_rate × impact × year_factor
      │
      ├─ Calculate Secondary SDG Effects
      │   └─ Using interdependency matrix
      │       └─ secondary_impact = primary × 0.3 × coefficient
      │
      ├─ Calculate Affected Population
      │   └─ population × sdg_coverage × impact_magnitude
      │
      └─ Calculate Confidence Score
          └─ Based on scenario, funding, timeline
      │
      ▼
   AI EXPLAINER
      │
      ├─ Generate Plain English Explanation
      │   └─ "If project succeeds, SDG 6 improves by X%..."
      │
      ├─ Generate Policy Insight
      │   └─ "Recommended action: Continue supporting..."
      │
      └─ Generate Risk Warning (if applicable)
          └─ "⚠️ Warning: X indicators show negative trends..."
      │
      ▼
   SAVE TO DATABASE
      │
      └─ Store in simulations table
      │
      ▼
   RETURN JSON RESPONSE
      │
      ▼
   FRONTEND RENDERING
      │
      ├─ Display Results Header
      │   └─ Confidence, Population, SDG Count
      │
      ├─ Display AI Explanation
      │
      ├─ Render SDG Impact Cards
      │   └─ For each SDG:
      │       ├─ Baseline vs Final value
      │       ├─ Chart.js timeline visualization
      │       └─ Change percentage badge
      │
      ├─ Display Secondary Effects
      │
      └─ Show Policy Insights & Warnings
```

---

## **Key Algorithms**

### **1. Impact Factor Calculation**

```python
# Base scenario multipliers
SCENARIO_MULTIPLIERS = {
    "success": 1.0,
    "partial_success": 0.6,
    "delay": 0.4,
    "failure": -0.2,
    "underfunded": 0.3
}

# Combined impact calculation
base_multiplier = SCENARIO_MULTIPLIERS[scenario_type]
funding_factor = funding_percentage / 100.0
delay_factor = max(0.2, 1.0 - (delay_months / 24.0))

impact_factor = base_multiplier × funding_factor × delay_factor × scale_factor
```

### **2. Yearly SDG Progression**

```python
for year in range(0, timeline_years + 1):
    # Diminishing returns over time
    year_factor = 1.0 - (year × 0.1)
    
    if lower_is_better:
        # Reduce negative indicators (poverty, emissions)
        annual_change = -baseline × 0.08 × impact_factor × year_factor
    else:
        # Increase positive indicators (education, water access)
        annual_change = baseline × 0.06 × impact_factor × year_factor
    
    # Add realistic noise
    noise = random.normal(0, abs(annual_change) × 0.1)
    
    current_value += annual_change + noise
```

### **3. Cross-SDG Dependencies**

```python
# Interdependency matrix
SDG_INTERDEPENDENCIES = {
    1: [2, 3, 4, 8, 10],  # Poverty affects hunger, health, education
    6: [2, 3, 11, 12],     # Water affects hunger, health, cities
    13: [2, 6, 11, 14, 15] # Climate affects multiple SDGs
}

# Calculate secondary impact
for primary_sdg in target_sdgs:
    affected_sdgs = SDG_INTERDEPENDENCIES[primary_sdg]
    for secondary_sdg in affected_sdgs:
        secondary_change = primary_change × 0.3 × interdependency_coefficient
```

### **4. Confidence Scoring**

```python
# Base confidence by scenario
scenario_confidence = {
    "success": 0.75,
    "failure": 0.70,
    "delay": 0.60
}

# Adjustments
timeline_penalty = max(0, 0.15 × (timeline_years - 3) / 5.0)
delay_penalty = min(0.2, delay_months / 60.0)
funding_bonus = 0.1 if funding_percentage >= 90 else 0

confidence = base - timeline_penalty - delay_penalty + funding_bonus
```

---

## **Database Schema**

### **Entity Relationship Diagram**

```
┌─────────────────┐
│ organizations   │
│─────────────────│
│ id (PK)         │
│ name            │
│ type            │
│ focus_sdgs      │
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼────────┐       ┌─────────────────┐
│   projects      │       │  digital_twins  │
│─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │
│ organization_id │◄──┐   │ name            │
│ digital_twin_id │───┼──►│ region          │
│ title           │   │   │ population      │
│ target_sdgs     │   │   │ baseline_year   │
└────────┬────────┘   │   └────────┬────────┘
         │            │            │
         │ 1:N        │            │ 1:N
         │            │            │
┌────────▼────────┐   │   ┌────────▼────────┐
│  simulations    │◄──┘   │ sdg_indicators  │
│─────────────────│       │─────────────────│
│ id (PK)         │       │ id (PK)         │
│ digital_twin_id │       │ digital_twin_id │
│ project_id      │       │ sdg_number      │
│ scenario_type   │       │ baseline_value  │
│ predicted_outcomes│      │ target_value    │
│ explanation     │       │ unit            │
│ confidence_score│       └─────────────────┘
└─────────────────┘

┌─────────────────┐
│  partnerships   │
│─────────────────│
│ id (PK)         │
│ requesting_org  │
│ target_org      │
│ project_id      │
│ status          │
└─────────────────┘
```

---

## **API Architecture**

### **RESTful Endpoints**

```
BASE URL: http://localhost:8000

Authentication: None (demo version)

Endpoints:
├── GET    /                          # API info
├── GET    /sdgs                      # Get all 17 SDGs
│
├── Digital Twins
│   ├── POST   /digital-twins         # Create digital twin
│   ├── GET    /digital-twins         # List all twins
│   └── GET    /digital-twins/{id}    # Get twin with indicators
│
├── Simulations ⭐ CORE INNOVATION
│   ├── POST   /simulations/run       # Run future simulation
│   ├── GET    /simulations/{id}      # Get simulation result
│   ├── GET    /simulations/digital-twin/{id}  # List by twin
│   └── POST   /simulations/compare   # Compare scenarios
│
├── Projects
│   ├── POST   /projects              # Create project
│   ├── GET    /projects              # List projects
│   └── GET    /projects/{id}         # Get project
│
├── Organizations
│   ├── POST   /organizations         # Register organization
│   ├── GET    /organizations         # List organizations
│   └── GET    /organizations/{id}    # Get organization
│
└── Partnerships
    ├── POST   /partnerships          # Create partnership
    └── GET    /partnerships/organization/{id}  # Get org partnerships

API Documentation: http://localhost:8000/docs (Swagger UI)
```

---

## **Frontend Architecture**

### **Component Structure**

```
index.html (Main Container)
│
├── Header
│   ├── Logo & Tagline
│   └── Navigation Tabs
│       ├── Digital Twins
│       ├── Future Simulation ⭐
│       ├── Projects
│       └── Organizations
│
├── Section: Digital Twins
│   ├── Create Button
│   └── Twins Grid (cards)
│
├── Section: Future Simulation ⭐ FLAGSHIP
│   ├── Simulation Controls Panel
│   │   ├── Twin Selector
│   │   ├── Project Selector
│   │   ├── SDG Chip Selector (17 chips)
│   │   ├── Scenario Buttons (5 scenarios)
│   │   ├── Funding Slider (0-100%)
│   │   ├── Timeline Slider (1-10 years)
│   │   ├── Delay Slider (0-36 months)
│   │   ├── Run Simulation Button
│   │   └── Compare Scenarios Button
│   │
│   └── Results Display Panel
│       ├── Results Header (confidence, population, SDG count)
│       ├── AI Explanation Box
│       ├── Policy Insight Box
│       ├── Risk Warning Box (conditional)
│       ├── Primary SDG Impact Cards
│       │   └── Chart.js Timeline (per SDG)
│       └── Secondary SDG Effects
│
├── Section: Projects
│   ├── Create Button
│   └── Projects Grid (cards)
│
├── Section: Organizations
│   ├── Create Button
│   └── Organizations Grid (cards)
│
└── Modals (overlays)
    ├── Create Digital Twin Modal
    ├── Create Organization Modal
    └── Create Project Modal
```

### **JavaScript Modules**

```javascript
app.js
│
├── Initialization
│   ├── loadSDGs()
│   ├── loadDigitalTwins()
│   ├── loadOrganizations()
│   ├── loadProjects()
│   └── setupEventListeners()
│
├── Navigation
│   └── setupNavigation() - Tab switching
│
├── Simulation Controls
│   ├── setupSliders() - Real-time value updates
│   ├── setupScenarioButtons() - Scenario selection
│   ├── toggleSDG() - SDG chip selection
│   └── loadTwinForSimulation() - Load twin data
│
├── Core Simulation ⭐
│   ├── runSimulation() - Execute prediction
│   ├── displaySimulationResults() - Render output
│   ├── renderTimelineChart() - Chart.js rendering
│   └── compareScenarios() - Multi-scenario comparison
│
├── CRUD Operations
│   ├── createDigitalTwin()
│   ├── createOrganization()
│   └── createProject()
│
└── UI Rendering
    ├── renderDigitalTwins()
    ├── renderOrganizations()
    ├── renderProjects()
    └── updateSelectors()
```

---

## **Technology Stack**

### **Backend**
- **Framework:** FastAPI 0.109.0
- **ORM:** SQLAlchemy 2.0.25
- **Database:** SQLite (demo) / MySQL / PostgreSQL (production)
- **Validation:** Pydantic 2.5.3
- **ML/Math:** NumPy 1.26.3, scikit-learn 1.4.0
- **Server:** Uvicorn 0.27.0

### **Frontend**
- **Core:** HTML5, CSS3, JavaScript (ES6+)
- **Charts:** Chart.js 4.4.0
- **Architecture:** Single Page Application (SPA)
- **No framework** - Vanilla JS for simplicity and speed

### **Database**
- **Development:** SQLite (file-based)
- **Production-ready:** MySQL 8.0+ or PostgreSQL 13+
- **Schema:** 6 tables with foreign key relationships

---

## **Deployment Architecture**

### **Development**
```
┌──────────────┐     ┌──────────────┐
│   Backend    │     │   Frontend   │
│ Port 8000    │◄────┤  Port 3000   │
│ Uvicorn      │     │  http.server │
└──────┬───────┘     └──────────────┘
       │
       ▼
┌──────────────┐
│  SQLite DB   │
│ (local file) │
└──────────────┘
```

### **Production** (Future)
```
┌─────────────────────────────────────┐
│         Load Balancer (NGINX)       │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼───┐
│Backend │      │Backend │
│Instance│      │Instance│
└───┬────┘      └────┬───┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │   PostgreSQL    │
    │   (Primary)     │
    └────────┬────────┘
             │
    ┌────────▼────────┐
    │   PostgreSQL    │
    │   (Replica)     │
    └─────────────────┘

Frontend: CDN (CloudFlare/AWS CloudFront)
```

---

## **Security Considerations**

### **Current (Demo)**
- No authentication (open API)
- No input sanitization beyond Pydantic validation
- CORS enabled for all origins

### **Production Requirements**
- JWT-based authentication
- Role-based access control (RBAC)
- API rate limiting
- Input sanitization and SQL injection prevention
- HTTPS/TLS encryption
- Environment variable management
- Database connection pooling
- Backup and disaster recovery

---

## **Performance Optimization**

### **Backend**
- Connection pooling for database
- Caching frequently accessed data (Redis)
- Async/await for I/O operations
- Database indexing on foreign keys
- Query optimization with joins

### **Frontend**
- Lazy loading for charts
- Debouncing on slider inputs
- Virtual scrolling for large lists
- Asset minification
- CDN for static assets

---

## **Scalability Path**

### **Horizontal Scaling**
- Stateless API design (ready for load balancing)
- Database read replicas
- Microservices architecture (future)
- Message queue for long simulations (Celery/RabbitMQ)

### **Vertical Scaling**
- Increase server resources
- Optimize algorithms
- Use compiled extensions (Cython)
- GPU acceleration for ML models

---

**This architecture is designed for demo excellence now, and production scale later.** 🚀
