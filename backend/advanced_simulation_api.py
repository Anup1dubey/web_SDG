"""
Advanced Simulation API Endpoint
Integrates the complete simulation engine with the FastAPI backend
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
import json

from database import get_db, DigitalTwin, Simulation
from sdg_graph import SDGIndicatorGraph
from simulation_core import TimeStepSimulationEngine
from simulation_explainer import SimulationExplainer

router = APIRouter(prefix="/api/simulation", tags=["advanced_simulation"])


class SimulationRequest(BaseModel):
    """Request model for running a simulation"""
    digital_twin_id: int
    target_sdgs: List[int]
    scenario_type: str  # 'success', 'partial_success', 'delay', 'failure', 'underfunded'
    funding_percentage: float = 100.0
    timeline_years: int = 5
    delay_months: int = 0
    project_id: Optional[int] = None


class YearlyState(BaseModel):
    """State for a single year"""
    year: int
    indicators: Dict[str, float]


class SimulationResponse(BaseModel):
    """Complete simulation result"""
    simulation_id: int
    digital_twin_id: int
    digital_twin_name: str
    target_sdgs: List[int]
    scenario_type: str
    timeline_years: int
    
    # Results
    yearly_states: List[YearlyState]
    net_sdg_progress: float
    confidence_score: float
    
    # Explanations
    narrative: str
    top_changes: List[Dict]
    bottlenecks: List[Dict]
    risk_factors: List[str]
    recommendations: List[str]
    
    # Metadata
    created_at: datetime
    effectiveness: float


@router.post("/run", response_model=SimulationResponse)
async def run_advanced_simulation(
    request: SimulationRequest,
    db: Session = Depends(get_db)
):
    """
    Run an advanced SDG Digital Twin simulation
    
    This endpoint uses the sophisticated simulation engine that includes:
    - SDG indicator interdependencies
    - Time-delayed effects
    - Diminishing returns
    - Constraints and trade-offs
    - Feedback loops
    - Scenario-based outcomes
    """
    
    # Validate digital twin exists
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == request.digital_twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    # Validate SDGs
    if not request.target_sdgs or len(request.target_sdgs) == 0:
        raise HTTPException(status_code=400, detail="At least one target SDG is required")
    
    for sdg in request.target_sdgs:
        if sdg < 1 or sdg > 17:
            raise HTTPException(status_code=400, detail=f"Invalid SDG number: {sdg}")
    
    # Validate scenario type
    valid_scenarios = ['success', 'partial_success', 'delay', 'failure', 'underfunded']
    if request.scenario_type not in valid_scenarios:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid scenario type. Must be one of: {', '.join(valid_scenarios)}"
        )
    
    # Initialize the simulation engine
    graph = SDGIndicatorGraph()
    
    engine = TimeStepSimulationEngine(
        graph=graph,
        target_sdgs=request.target_sdgs,
        scenario_type=request.scenario_type,
        funding_percentage=request.funding_percentage,
        timeline_years=request.timeline_years,
        delay_months=request.delay_months
    )
    
    # Run the simulation
    states = engine.run_simulation()
    
    # Generate explanations
    explainer = SimulationExplainer(
        graph=graph,
        states=states,
        constraint_engine=engine.constraint_engine,
        target_sdgs=request.target_sdgs
    )
    
    summary = explainer.generate_summary()
    
    # Save simulation to database (matching existing schema)
    simulation = Simulation(
        digital_twin_id=request.digital_twin_id,
        project_id=request.project_id,
        scenario_type=request.scenario_type,
        simulation_name=f"Advanced {request.scenario_type.title()} Scenario",
        funding_percentage=request.funding_percentage,
        timeline_years=request.timeline_years,
        delay_months=request.delay_months,
        scale_factor=1.0,
        predicted_outcomes={
            'yearly_states': [
                {'year': state.year, 'indicators': state.indicators}
                for state in states
            ],
            'summary': summary
        },
        affected_population=twin.population,
        confidence_score=summary['confidence_score'],
        explanation=summary['narrative'],
        policy_insight='\n'.join(summary['recommendations']),
        risk_warning='\n'.join(summary['risks'])
    )
    
    db.add(simulation)
    db.commit()
    db.refresh(simulation)
    
    # Build response
    return SimulationResponse(
        simulation_id=simulation.id,
        digital_twin_id=twin.id,
        digital_twin_name=twin.name,
        target_sdgs=request.target_sdgs,
        scenario_type=request.scenario_type,
        timeline_years=request.timeline_years,
        yearly_states=[
            YearlyState(year=state.year, indicators=state.indicators)
            for state in states
        ],
        net_sdg_progress=summary['net_sdg_progress'],
        confidence_score=summary['confidence_score'],
        narrative=summary['narrative'],
        top_changes=summary['top_changes'],
        bottlenecks=summary['bottlenecks'],
        risk_factors=summary['risks'],
        recommendations=summary['recommendations'],
        created_at=simulation.created_at,
        effectiveness=summary['effectiveness']
    )


@router.get("/history/{digital_twin_id}")
async def get_simulation_history(
    digital_twin_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get simulation history for a digital twin"""
    
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == digital_twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    simulations = db.query(Simulation).filter(
        Simulation.digital_twin_id == digital_twin_id
    ).order_by(Simulation.created_at.desc()).limit(limit).all()
    
    return {
        'digital_twin_id': digital_twin_id,
        'digital_twin_name': twin.name,
        'simulations': [
            {
                'simulation_id': sim.id,
                'scenario_type': sim.scenario_type,
                'target_sdgs': sim.target_sdgs,
                'confidence_score': sim.confidence_score,
                'created_at': sim.created_at,
                'net_progress': sim.results.get('summary', {}).get('net_sdg_progress', 0)
            }
            for sim in simulations
        ]
    }


@router.get("/compare/{simulation_id_1}/{simulation_id_2}")
async def compare_simulations(
    simulation_id_1: int,
    simulation_id_2: int,
    db: Session = Depends(get_db)
):
    """Compare two simulations side by side"""
    
    sim1 = db.query(Simulation).filter(Simulation.id == simulation_id_1).first()
    sim2 = db.query(Simulation).filter(Simulation.id == simulation_id_2).first()
    
    if not sim1 or not sim2:
        raise HTTPException(status_code=404, detail="One or both simulations not found")
    
    if sim1.digital_twin_id != sim2.digital_twin_id:
        raise HTTPException(
            status_code=400, 
            detail="Can only compare simulations from the same digital twin"
        )
    
    return {
        'digital_twin_id': sim1.digital_twin_id,
        'simulation_1': {
            'id': sim1.id,
            'scenario': sim1.scenario_type,
            'net_progress': sim1.results.get('summary', {}).get('net_sdg_progress', 0),
            'confidence': sim1.confidence_score,
            'narrative': sim1.results.get('summary', {}).get('narrative', '')
        },
        'simulation_2': {
            'id': sim2.id,
            'scenario': sim2.scenario_type,
            'net_progress': sim2.results.get('summary', {}).get('net_sdg_progress', 0),
            'confidence': sim2.confidence_score,
            'narrative': sim2.results.get('summary', {}).get('narrative', '')
        },
        'comparison': {
            'progress_difference': (
                sim1.results.get('summary', {}).get('net_sdg_progress', 0) -
                sim2.results.get('summary', {}).get('net_sdg_progress', 0)
            ),
            'better_scenario': sim1.scenario_type if 
                sim1.results.get('summary', {}).get('net_sdg_progress', 0) > 
                sim2.results.get('summary', {}).get('net_sdg_progress', 0)
                else sim2.scenario_type
        }
    }


@router.post("/batch-scenarios/{digital_twin_id}")
async def run_all_scenarios(
    digital_twin_id: int,
    target_sdgs: List[int],
    timeline_years: int = 5,
    db: Session = Depends(get_db)
):
    """
    Run simulations for all scenario types to compare outcomes
    Useful for policy decision making
    """
    
    twin = db.query(DigitalTwin).filter(DigitalTwin.id == digital_twin_id).first()
    if not twin:
        raise HTTPException(status_code=404, detail="Digital twin not found")
    
    scenarios = ['success', 'partial_success', 'delay', 'failure', 'underfunded']
    results = []
    
    graph = SDGIndicatorGraph()
    
    for scenario in scenarios:
        # Run simulation
        engine = TimeStepSimulationEngine(
            graph=graph,
            target_sdgs=target_sdgs,
            scenario_type=scenario,
            funding_percentage=100.0 if scenario != 'underfunded' else 50.0,
            timeline_years=timeline_years,
            delay_months=0 if scenario != 'delay' else 12
        )
        
        states = engine.run_simulation()
        
        # Generate summary
        explainer = SimulationExplainer(
            graph=graph,
            states=states,
            constraint_engine=engine.constraint_engine,
            target_sdgs=target_sdgs
        )
        
        summary = explainer.generate_summary()
        
        results.append({
            'scenario': scenario,
            'net_progress': summary['net_sdg_progress'],
            'confidence': summary['confidence_score'],
            'narrative': summary['narrative'],
            'final_state': states[-1].indicators
        })
    
    # Sort by net progress
    results.sort(key=lambda x: x['net_progress'], reverse=True)
    
    return {
        'digital_twin_id': digital_twin_id,
        'digital_twin_name': twin.name,
        'target_sdgs': target_sdgs,
        'timeline_years': timeline_years,
        'scenarios': results,
        'best_scenario': results[0]['scenario'],
        'worst_scenario': results[-1]['scenario']
    }
