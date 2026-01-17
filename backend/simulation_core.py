"""
Advanced Time-Step Simulation Engine
Simulates year-by-year progression with delayed effects, diminishing returns, and constraints
"""
from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass, field
from copy import deepcopy
from sdg_graph import SDGIndicatorGraph, IndicatorInfluence


@dataclass
class SimulationState:
    """Represents the state of all indicators at a specific year"""
    year: int
    indicators: Dict[str, float]
    delayed_effects: List[Tuple[str, float, int]] = field(default_factory=list)  # (indicator, effect, years_left)
    
    def clone(self):
        """Create a deep copy of this state"""
        return SimulationState(
            year=self.year,
            indicators=deepcopy(self.indicators),
            delayed_effects=deepcopy(self.delayed_effects)
        )


@dataclass
class Constraint:
    """Represents a constraint that limits impact"""
    name: str
    factor: float  # 0.0 to 1.0, multiplier on effectiveness
    description: str


class SaturationFunction:
    """
    Implements diminishing returns using logistic curve
    Impact reduces as indicator approaches its natural limit
    """
    
    @staticmethod
    def apply(current_value: float, potential_change: float, max_value: float, 
              min_value: float = 0.0, steepness: float = 0.1) -> float:
        """
        Apply saturation to a potential change
        
        Args:
            current_value: Current indicator value
            potential_change: Proposed change (can be positive or negative)
            max_value: Maximum possible value
            min_value: Minimum possible value
            steepness: Controls how quickly saturation kicks in
            
        Returns:
            Actual change after saturation
        """
        if potential_change == 0:
            return 0
        
        # For positive changes (improvements)
        if potential_change > 0:
            # Distance to ceiling
            distance_to_max = max_value - current_value
            if distance_to_max <= 0:
                return 0
            
            # Saturation factor: easier to improve when far from max
            # Uses sigmoid-like curve
            normalized_distance = distance_to_max / max_value
            saturation_factor = 1 / (1 + np.exp(-10 * (normalized_distance - 0.5)))
            
            # Apply diminishing returns
            actual_change = potential_change * saturation_factor
            
            # Ensure we don't exceed max
            return min(actual_change, distance_to_max)
        
        # For negative changes (degradation)
        else:
            # Distance to floor
            distance_to_min = current_value - min_value
            if distance_to_min <= 0:
                return 0
            
            # Negative changes are less saturated (degradation can be rapid)
            return max(potential_change, -distance_to_min)


class ConstraintEngine:
    """Manages and applies constraints to simulation"""
    
    def __init__(self, scenario_type: str, funding_percentage: float, 
                 timeline_years: int, delay_months: int):
        self.constraints = self._build_constraints(
            scenario_type, funding_percentage, timeline_years, delay_months
        )
    
    def _build_constraints(self, scenario_type: str, funding_percentage: float,
                          timeline_years: int, delay_months: int) -> List[Constraint]:
        """Build constraints based on scenario and parameters"""
        constraints = []
        
        # Funding constraint
        funding_factor = funding_percentage / 100.0
        constraints.append(Constraint(
            name='Funding Limitation',
            factor=funding_factor,
            description=f'Project is {funding_percentage}% funded, reducing effective impact'
        ))
        
        # Timeline constraint (rushed projects are less effective)
        if timeline_years < 3:
            timeline_factor = 0.7  # Rushed
        elif timeline_years > 7:
            timeline_factor = 0.9  # Well-paced
        else:
            timeline_factor = 1.0  # Optimal
        
        constraints.append(Constraint(
            name='Timeline Pressure',
            factor=timeline_factor,
            description=f'{timeline_years}-year timeline affects implementation quality'
        ))
        
        # Delay constraint
        delay_years = delay_months / 12.0
        if delay_years > 0:
            delay_factor = max(0.5, 1.0 - (delay_years / 3.0))  # Each year of delay reduces effectiveness
            constraints.append(Constraint(
                name='Implementation Delay',
                factor=delay_factor,
                description=f'{delay_months}-month delay reduces early impact'
            ))
        
        # Scenario-specific constraints
        if scenario_type == 'success':
            constraints.append(Constraint(
                name='Optimal Conditions',
                factor=1.0,
                description='Ideal implementation conditions'
            ))
        
        elif scenario_type == 'partial_success':
            constraints.append(Constraint(
                name='Partial Implementation',
                factor=0.7,
                description='Some objectives achieved, others delayed'
            ))
        
        elif scenario_type == 'delay':
            constraints.append(Constraint(
                name='Major Delays',
                factor=0.5,
                description='Significant implementation delays reduce impact'
            ))
        
        elif scenario_type == 'failure':
            constraints.append(Constraint(
                name='Implementation Failure',
                factor=0.2,
                description='Project largely failed, minimal impact achieved'
            ))
        
        elif scenario_type == 'underfunded':
            constraints.append(Constraint(
                name='Severe Underfunding',
                factor=0.4,
                description='Insufficient resources limit implementation'
            ))
        
        # Infrastructure readiness constraint (random but bounded)
        infrastructure_factor = np.random.uniform(0.8, 1.0)
        constraints.append(Constraint(
            name='Infrastructure Readiness',
            factor=infrastructure_factor,
            description=f'Infrastructure readiness affects implementation ({infrastructure_factor:.1%})'
        ))
        
        return constraints
    
    def apply_constraints(self, base_impact: float) -> Tuple[float, List[str]]:
        """
        Apply all constraints to a base impact value
        
        Returns:
            Tuple of (constrained_impact, list of active constraint descriptions)
        """
        constrained_impact = base_impact
        active_constraints = []
        
        for constraint in self.constraints:
            if constraint.factor < 1.0:
                constrained_impact *= constraint.factor
                active_constraints.append(constraint.description)
        
        return constrained_impact, active_constraints
    
    def get_total_effectiveness(self) -> float:
        """Get the combined effectiveness factor from all constraints"""
        total = 1.0
        for constraint in self.constraints:
            total *= constraint.factor
        return total


class FeedbackLoopEngine:
    """
    Implements positive and negative feedback loops
    Feedback effects accumulate over time and influence future states
    """
    
    def __init__(self, graph: SDGIndicatorGraph):
        self.graph = graph
        self.feedback_loops = self._define_feedback_loops()
    
    def _define_feedback_loops(self) -> List[Dict]:
        """Define key feedback loops in the system"""
        return [
            {
                'name': 'Education-Employment-Revenue Loop',
                'chain': ['education_index', 'employment_rate', 'governance_index', 'education_index'],
                'type': 'positive',
                'strength': 0.15,
                'delay': 2,
                'description': 'Better education → more employment → higher tax revenue → more education funding'
            },
            {
                'name': 'Industrial-Emissions-Health Loop',
                'chain': ['innovation_index', 'emissions_reduction', 'health_index', 'employment_rate'],
                'type': 'mixed',
                'strength': -0.10,
                'delay': 3,
                'description': 'Industrial growth can increase emissions, reducing health and productivity'
            },
            {
                'name': 'Poverty-Health-Employment Trap',
                'chain': ['poverty_rate', 'health_index', 'employment_rate', 'poverty_rate'],
                'type': 'negative',
                'strength': -0.12,
                'delay': 1,
                'description': 'Poverty reduces health access, limiting employment, perpetuating poverty'
            },
            {
                'name': 'Clean Energy Innovation Loop',
                'chain': ['clean_energy', 'innovation_index', 'employment_rate', 'clean_energy'],
                'type': 'positive',
                'strength': 0.18,
                'delay': 2,
                'description': 'Clean energy drives innovation, creating jobs, enabling more clean energy investment'
            },
        ]
    
    def calculate_feedback_effects(self, state: SimulationState, 
                                   previous_states: List[SimulationState]) -> Dict[str, float]:
        """
        Calculate feedback effects based on historical states
        
        Returns:
            Dictionary of indicator -> feedback effect value
        """
        feedback_effects = {}
        
        if len(previous_states) < 2:
            return feedback_effects  # Need history for feedback
        
        for loop in self.feedback_loops:
            delay = loop['delay']
            
            # Check if we have enough history
            if len(previous_states) < delay:
                continue
            
            # Get the state from 'delay' years ago
            historical_state = previous_states[-delay] if delay <= len(previous_states) else previous_states[0]
            
            # Calculate the change in the feedback chain
            chain_strength = 1.0
            for i in range(len(loop['chain']) - 1):
                indicator = loop['chain'][i]
                
                current_val = state.indicators.get(indicator, 0)
                historical_val = historical_state.indicators.get(indicator, 0)
                
                # Normalized change
                change = (current_val - historical_val) / 100.0
                chain_strength *= (1.0 + change * loop['strength'])
            
            # Apply feedback to the last indicator in the chain
            target_indicator = loop['chain'][-1]
            feedback_effect = (chain_strength - 1.0) * 100.0 * loop['strength']
            
            feedback_effects[target_indicator] = feedback_effects.get(target_indicator, 0) + feedback_effect
        
        return feedback_effects


class TimeStepSimulationEngine:
    """
    Core simulation engine that runs year-by-year simulations
    """
    
    def __init__(self, graph: SDGIndicatorGraph, target_sdgs: List[int],
                 scenario_type: str, funding_percentage: float,
                 timeline_years: int, delay_months: int):
        self.graph = graph
        self.target_sdgs = target_sdgs
        self.timeline_years = timeline_years
        
        # Initialize engines
        self.constraint_engine = ConstraintEngine(
            scenario_type, funding_percentage, timeline_years, delay_months
        )
        self.feedback_engine = FeedbackLoopEngine(graph)
        self.saturation = SaturationFunction()
        
        # Simulation history
        self.states: List[SimulationState] = []
    
    def initialize_baseline(self, digital_twin_data: Dict = None) -> SimulationState:
        """Initialize Year 0 baseline state"""
        indicators = {}
        
        for indicator_key, indicator_info in self.graph.indicators.items():
            # Use digital twin specific data if available, otherwise use defaults
            if digital_twin_data and indicator_key in digital_twin_data:
                indicators[indicator_key] = digital_twin_data[indicator_key]
            else:
                indicators[indicator_key] = indicator_info['baseline']
        
        return SimulationState(year=0, indicators=indicators, delayed_effects=[])
    
    def calculate_direct_impact(self, target_sdgs: List[int]) -> Dict[str, float]:
        """
        Calculate direct project impact on target SDGs
        Base impact before constraints and saturation
        """
        direct_impacts = {}
        
        for sdg_num in target_sdgs:
            sdg_indicators = self.graph.get_sdg_indicators(sdg_num)
            
            for indicator in sdg_indicators:
                # Base improvement from targeting this SDG
                base_improvement = np.random.uniform(8.0, 15.0)  # 8-15% improvement potential
                direct_impacts[indicator] = direct_impacts.get(indicator, 0) + base_improvement
        
        return direct_impacts
    
    def simulate_year(self, current_state: SimulationState, year: int,
                     direct_impacts: Dict[str, float]) -> SimulationState:
        """Simulate a single year, returning the new state"""
        new_state = current_state.clone()
        new_state.year = year
        
        changes_made = {}  # Track what changed and why
        
        # 1. Apply direct project impacts (with constraints and saturation)
        effectiveness = self.constraint_engine.get_total_effectiveness()
        
        for indicator, base_impact in direct_impacts.items():
            # Apply constraints
            constrained_impact = base_impact * effectiveness
            
            # Apply saturation
            current_val = new_state.indicators[indicator]
            indicator_info = self.graph.get_indicator_info(indicator)
            
            actual_change = self.saturation.apply(
                current_val, constrained_impact,
                indicator_info['max'], indicator_info['min']
            )
            
            new_state.indicators[indicator] += actual_change
            changes_made[indicator] = changes_made.get(indicator, 0) + actual_change
        
        # 2. Apply delayed effects from previous years
        remaining_delays = []
        for indicator, effect, years_left in new_state.delayed_effects:
            if years_left <= 1:
                # Effect kicks in this year
                current_val = new_state.indicators[indicator]
                indicator_info = self.graph.get_indicator_info(indicator)
                
                actual_change = self.saturation.apply(
                    current_val, effect,
                    indicator_info['max'], indicator_info['min']
                )
                
                new_state.indicators[indicator] += actual_change
                changes_made[indicator] = changes_made.get(indicator, 0) + actual_change
            else:
                # Still waiting
                remaining_delays.append((indicator, effect, years_left - 1))
        
        new_state.delayed_effects = remaining_delays
        
        # 3. Calculate and apply indirect effects via SDG graph
        for indicator, change in list(changes_made.items()):
            if abs(change) < 0.1:  # Skip tiny changes
                continue
            
            influences = self.graph.get_influences_from(indicator)
            
            for influence in influences:
                # Calculate indirect effect
                indirect_effect = change * influence.weight
                
                if influence.delay_years > 0:
                    # Add to delayed effects
                    new_state.delayed_effects.append((
                        influence.target, indirect_effect, influence.delay_years
                    ))
                else:
                    # Apply immediately
                    current_val = new_state.indicators[influence.target]
                    target_info = self.graph.get_indicator_info(influence.target)
                    
                    actual_change = self.saturation.apply(
                        current_val, indirect_effect,
                        target_info['max'], target_info['min']
                    )
                    
                    new_state.indicators[influence.target] += actual_change
                    changes_made[influence.target] = changes_made.get(influence.target, 0) + actual_change
        
        # 4. Apply feedback loop effects
        if len(self.states) > 0:
            feedback_effects = self.feedback_engine.calculate_feedback_effects(
                new_state, self.states
            )
            
            for indicator, feedback in feedback_effects.items():
                current_val = new_state.indicators[indicator]
                indicator_info = self.graph.get_indicator_info(indicator)
                
                actual_change = self.saturation.apply(
                    current_val, feedback,
                    indicator_info['max'], indicator_info['min']
                )
                
                new_state.indicators[indicator] += actual_change
        
        # 5. Ensure all values stay within bounds
        for indicator, value in new_state.indicators.items():
            indicator_info = self.graph.get_indicator_info(indicator)
            new_state.indicators[indicator] = np.clip(
                value, indicator_info['min'], indicator_info['max']
            )
        
        return new_state
    
    def run_simulation(self, baseline_state: SimulationState = None) -> List[SimulationState]:
        """
        Run the complete multi-year simulation
        
        Returns:
            List of states for each year (Year 0 to Year N)
        """
        # Initialize
        if baseline_state is None:
            baseline_state = self.initialize_baseline()
        
        self.states = [baseline_state]
        
        # Calculate direct impacts once (these are the project's intended effects)
        direct_impacts = self.calculate_direct_impact(self.target_sdgs)
        
        # Simulate each year
        for year in range(1, self.timeline_years + 1):
            current_state = self.states[-1]
            next_state = self.simulate_year(current_state, year, direct_impacts)
            self.states.append(next_state)
        
        return self.states
