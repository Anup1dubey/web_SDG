"""
SDG Digital Twin Platform - FastAPI Backend
Core Innovation: Future Impact Simulation Engine
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import (
    init_db, get_db, Organization, DigitalTwin, SDGIndicator, 
    Project, Simulation, Partnership, User
)
from sdg_data import SDG_GOALS, SDG_INDICATORS, get_baseline_for_region
from simulation_engine import SimulationEngine, AIExplainer
from auth_routes import router as auth_router
from advanced_simulation_api import router as advanced_simulation_router

app = FastAPI(title="SDG Digital Twin Platform API", version="1.0.0")

# Include authentication routes
app.include_router(auth_router)

# Include advanced simulation routes
app.include_router(advanced_simulation_router)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize simulation engine
simulation_engine = SimulationEngine()
ai_explainer = AIExplainer()

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()


# ==================== Pydantic Models ====================

class OrganizationCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    focus_sdgs: List[int] = []

class OrganizationResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    focus_sdgs: List[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class DigitalTwinCreate(BaseModel):
    name: str
    region: str
    country: str
    population: int
    area_km2: float
    description: Optional[str] = None
    region_type: str = "developing_urban"  # For baseline template

class DigitalTwinResponse(BaseModel):
    id: int
    name: str
    region: str
    country: str
    population: int
    area_km2: float
    description: Optional[str]
    baseline_year: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    organization_id: int
    digital_twin_id: Optional[int] = None
    title: str
    description: str
    target_sdgs: List[int]
    budget: float
    timeline_months: int
    status: str = "Planning"

class ProjectResponse(BaseModel):
    id: int
    organization_id: int
    digital_twin_id: Optional[int]
    title: str
    description: str
    target_sdgs: List[int]
    budget: float
    timeline_months: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SimulationRequest(BaseModel):
    digital_twin_id: int
    project_id: Optional[int] = None
    scenario_type: str
    simulation_name: Optional[str] = None
    target_sdgs: List[int]
    funding_percentage: float = 100.0
    timeline_years: int = 5
    delay_months: int = 0
    scale_factor: float = 1.0

class SimulationResponse(BaseModel):
    id: int
    digital_twin_id: int
    project_id: Optional[int]
    scenario_type: str
    simulation_name: Optional[str]
    funding_percentage: float
    timeline_years: int
    delay_months: int
    predicted_outcomes: dict
    affected_population: int
    confidence_score: float
    explanation: str
    policy_insight: str
    risk_warning: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ==================== API Endpoints ====================

@app.get("/")
def root():
    return {
        "message": "SDG Digital Twin & Future Impact Simulation Platform",
        "version": "1.0.0",
        "innovation": "Predict future SDG outcomes before they happen"
    }

@app.get("/sdgs")
def get_sdgs():
    """Get all 17 SDGs with their indicators"""
    return {
        "goals": SDG_GOALS,
        "indicators": SDG_INDICATORS
    }


# ==================== Organizations ====================

@app.post("/organizations", response_model=OrganizationResponse)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    """Create a new organization"""
    db_org = Organization(**org.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@app.get("/organizations", response_model=List[OrganizationResponse])
def list_organizations(db: Session = Depends(get_db)):
    """List all organizations"""
    return db.query(Organization).all()

@app.get("/organizations/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Get organization by ID"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


# ==================== Digital Twins (CORE) ====================

@app.post("/digital-twins", response_model=DigitalTwinResponse)
def create_digital_twin(twin: DigitalTwinCreate, db: Session = Depends(get_db)):
    """Create a new Digital Twin with baseline SDG indicators"""
    
    # Create digital twin
    db_twin = DigitalTwin(
        name=twin.name,
        region=twin.region,
        country=twin.country,
        population=twin.population,
        area_km2=twin.area_km2,
        description=twin.description
    )
    db.add(db_twin)
    db.commit()
    db.refresh(db_twin)
    
    # Initialize baseline SDG indicators
    baseline_values = get_baseline_for_region(twin.region_type)
    
    for sdg_num in range(1, 18):
        indicator_info = SDG_INDICATORS.get(sdg_num, {})
        indicator = SDGIndicator(
            digital_twin_id=db_twin.id,
            sdg_number=sdg_num,
            sdg_name=SDG_GOALS[sdg_num],
            indicator_code=indicator_info.get("code", f"SDG{sdg_num}"),
            indicator_name=indicator_info.get("name", ""),
            baseline_value=baseline_values.get(sdg_num, 0),
            unit=indicator_info.get("unit", ""),
            target_value=baseline_values.get(sdg_num, 0) * 1.2  # 20% improvement target
        )
        db.add(indicator)
    
    db.commit()
    db.refresh(db_twin)
    return db_twin

@app.get("/digital-twins", response_model=List[DigitalTwinResponse])
def list_digital_twins(db: Session = Depends(get_db)):
    """List all Digital Twins"""
    return db.query(DigitalTwin).all()

@app.get("/digital-twins/{twin_id}")
def get_digital_twin(twin_id: int, db: Session = Depends(get_db)):
    """Get Digital Twin with all indicators"""
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital Twin not found")
    
    indicators = db.query(SDGIndicator).filter(SDGIndicator.digital_twin_id == twin_id).all()
    
    return {
        "twin": twin,
        "indicators": [
            {
                "sdg_number": ind.sdg_number,
                "sdg_name": ind.sdg_name,
                "baseline_value": ind.baseline_value,
                "unit": ind.unit,
                "target_value": ind.target_value
            }
            for ind in indicators
        ]
    }


# ==================== Simulations (CORE INNOVATION) ====================

@app.post("/simulations/run", response_model=SimulationResponse)
def run_simulation(request: SimulationRequest, db: Session = Depends(get_db)):
    """
    Run Future Impact Simulation - CORE INNOVATION
    Predicts what will happen to SDG indicators over time
    """
    
    # Get digital twin and its indicators
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == request.digital_twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital Twin not found")
    
    indicators = db.query(SDGIndicator).filter(
        SDGIndicator.digital_twin_id == request.digital_twin_id
    ).all()
    
    baseline_indicators = {ind.sdg_number: ind.baseline_value for ind in indicators}
    
    # Run simulation
    predicted_outcomes, affected_population, confidence = simulation_engine.simulate_future_impact(
        baseline_indicators=baseline_indicators,
        target_sdgs=request.target_sdgs,
        scenario_type=request.scenario_type,
        funding_percentage=request.funding_percentage,
        timeline_years=request.timeline_years,
        delay_months=request.delay_months,
        scale_factor=request.scale_factor,
        population=twin.population
    )
    
    # Generate AI explanation
    explanation, policy_insight, risk_warning = ai_explainer.generate_explanation(
        scenario_type=request.scenario_type,
        predicted_outcomes=predicted_outcomes,
        affected_population=affected_population,
        timeline_years=request.timeline_years,
        delay_months=request.delay_months,
        funding_percentage=request.funding_percentage
    )
    
    # Save simulation
    db_simulation = Simulation(
        digital_twin_id=request.digital_twin_id,
        project_id=request.project_id,
        scenario_type=request.scenario_type,
        simulation_name=request.simulation_name or f"{request.scenario_type.title()} Scenario",
        funding_percentage=request.funding_percentage,
        timeline_years=request.timeline_years,
        delay_months=request.delay_months,
        scale_factor=request.scale_factor,
        predicted_outcomes=predicted_outcomes,
        affected_population=affected_population,
        confidence_score=confidence,
        explanation=explanation,
        policy_insight=policy_insight,
        risk_warning=risk_warning
    )
    
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    
    return db_simulation

@app.get("/simulations/{simulation_id}", response_model=SimulationResponse)
def get_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Get simulation results by ID"""
    sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return sim

@app.get("/simulations/digital-twin/{twin_id}")
def list_simulations_for_twin(twin_id: int, db: Session = Depends(get_db)):
    """List all simulations for a digital twin"""
    sims = db.query(Simulation).filter(Simulation.digital_twin_id == twin_id).all()
    return sims

@app.post("/simulations/compare")
def compare_scenarios(
    digital_twin_id: int,
    target_sdgs: List[int],
    scenarios: List[str],
    funding_percentage: float = 100.0,
    timeline_years: int = 5,
    db: Session = Depends(get_db)
):
    """Compare multiple scenarios side-by-side"""
    
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == digital_twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital Twin not found")
    
    indicators = db.query(SDGIndicator).filter(
        SDGIndicator.digital_twin_id == digital_twin_id
    ).all()
    
    baseline_indicators = {ind.sdg_number: ind.baseline_value for ind in indicators}
    
    results = simulation_engine.compare_scenarios(
        baseline_indicators=baseline_indicators,
        target_sdgs=target_sdgs,
        scenarios=scenarios,
        funding_percentage=funding_percentage,
        timeline_years=timeline_years,
        population=twin.population
    )
    
    return results


# ==================== Projects ====================

@app.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new SDG project"""
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects", response_model=List[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    """List all projects"""
    return db.query(Project).all()

@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get project by ID"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# ==================== Partnerships ====================

@app.post("/partnerships")
def create_partnership(
    requesting_org_id: int,
    target_org_id: int,
    project_id: int,
    message: str,
    db: Session = Depends(get_db)
):
    """Create partnership request"""
    partnership = Partnership(
        requesting_org_id=requesting_org_id,
        target_org_id=target_org_id,
        project_id=project_id,
        message=message
    )
    db.add(partnership)
    db.commit()
    db.refresh(partnership)
    return partnership

@app.get("/partnerships/organization/{org_id}")
def get_organization_partnerships(org_id: int, db: Session = Depends(get_db)):
    """Get all partnerships for an organization"""
    partnerships = db.query(Partnership).filter(
        (Partnership.requesting_org_id == org_id) | (Partnership.target_org_id == org_id)
    ).all()
    return partnerships


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
