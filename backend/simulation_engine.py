"""
SDG Future Impact Simulation Engine
Core innovation: Predict future SDG outcomes based on project scenarios
"""
import random
from typing import Dict, List, Tuple
from sdg_data import SDG_INDICATORS, SDG_GOALS


class SimulationEngine:
    """
    Simulates future SDG impact using rule-based logic and lightweight ML
    """
    
    # Impact coefficients for different scenarios (how much SDGs change)
    SCENARIO_MULTIPLIERS = {
        "success": 1.0,
        "partial_success": 0.6,
        "delay": 0.4,
        "failure": -0.2,
        "underfunded": 0.3
    }
    
    # Cross-SDG influence matrix (simplified)
    # How much improving one SDG affects others
    SDG_INTERDEPENDENCIES = {
        1: [2, 3, 4, 8, 10],  # Poverty affects hunger, health, education, employment
        2: [1, 3, 12],
        3: [1, 2, 4, 6],
        4: [1, 5, 8, 10],
        5: [1, 4, 8, 10],
        6: [2, 3, 11, 12],
        7: [8, 9, 11, 13],
        8: [1, 4, 9, 10],
        9: [7, 8, 11, 12],
        10: [1, 5, 8, 16],
        11: [6, 7, 12, 13],
        12: [6, 11, 13, 14, 15],
        13: [2, 6, 11, 14, 15],
        14: [2, 12, 13],
        15: [2, 12, 13],
        16: [1, 10, 17],
        17: [1, 8, 9, 16]
    }
    
    def simulate_future_impact(
        self,
        baseline_indicators: Dict[int, float],
        target_sdgs: List[int],
        scenario_type: str,
        funding_percentage: float,
        timeline_years: int,
        delay_months: int = 0,
        scale_factor: float = 1.0,
        population: int = 100000
    ) -> Tuple[Dict[int, Dict], int, float]:
        """
        Simulate future SDG indicators based on project parameters
        
        Returns:
            - predicted_outcomes: Dict of SDG changes over time
            - affected_population: Number of people impacted
            - confidence_score: Simulation confidence (0-1)
        """
        
        # Initialize results
        predicted_outcomes = {}
        
        # Base multiplier from scenario type
        base_multiplier = self.SCENARIO_MULTIPLIERS.get(scenario_type, 0.5)
        
        # Adjust for funding and delays
        funding_factor = funding_percentage / 100.0
        delay_factor = max(0.2, 1.0 - (delay_months / 24.0))  # Max 2 years delay impact
        
        # Combined impact factor
        impact_factor = base_multiplier * funding_factor * delay_factor * scale_factor
        
        # Simulate each target SDG
        for sdg in target_sdgs:
            if sdg not in baseline_indicators:
                continue
                
            baseline = baseline_indicators[sdg]
            indicator_info = SDG_INDICATORS.get(sdg, {})
            lower_is_better = indicator_info.get("lower_is_better", False)
            
            # Calculate yearly progression
            yearly_changes = []
            current_value = baseline
            
            for year in range(timeline_years + 1):
                if year == 0:
                    yearly_changes.append({"year": year, "value": current_value})
                    continue
                
                # Calculate change (with diminishing returns over time)
                year_factor = 1.0 - (year * 0.1)  # Diminishing returns
                
                if lower_is_better:
                    # For negative indicators (poverty, emissions), reduce them
                    annual_change = -baseline * 0.08 * impact_factor * year_factor
                else:
                    # For positive indicators (education, water access), increase them
                    annual_change = baseline * 0.06 * impact_factor * year_factor
                
                # Add some realistic noise
                noise = random.gauss(0, abs(annual_change) * 0.1)
                current_value += annual_change + noise
                
                # Keep within realistic bounds
                if indicator_info.get("unit") == "%":
                    current_value = max(0, min(100, current_value))
                elif lower_is_better:
                    current_value = max(0, current_value)
                
                yearly_changes.append({
                    "year": year,
                    "value": round(current_value, 2),
                    "change": round(current_value - baseline, 2)
                })
            
            predicted_outcomes[sdg] = {
                "sdg_name": SDG_GOALS[sdg],
                "baseline": round(baseline, 2),
                "final": round(current_value, 2),
                "change": round(current_value - baseline, 2),
                "unit": indicator_info.get("unit", ""),
                "timeline": yearly_changes
            }
        
        # Simulate secondary impacts (cross-SDG effects)
        secondary_impacts = self._calculate_secondary_impacts(
            target_sdgs, 
            baseline_indicators, 
            impact_factor * 0.3  # Secondary effects are weaker
        )
        predicted_outcomes.update(secondary_impacts)
        
        # Calculate affected population
        # More SDGs + higher impact = more people affected
        impact_magnitude = abs(impact_factor)
        sdg_coverage = len(target_sdgs) / 17.0
        affected_population = int(population * sdg_coverage * impact_magnitude)
        
        # Confidence score based on funding, timeline, and scenario
        confidence = self._calculate_confidence(
            scenario_type, funding_percentage, timeline_years, delay_months
        )
        
        return predicted_outcomes, affected_population, confidence
    
    def _calculate_secondary_impacts(
        self, 
        primary_sdgs: List[int], 
        baseline_indicators: Dict[int, float],
        impact_factor: float
    ) -> Dict[int, Dict]:
        """Calculate ripple effects on related SDGs"""
        secondary = {}
        affected_secondary_sdgs = set()
        
        # Find all SDGs influenced by primary targets
        for sdg in primary_sdgs:
            if sdg in self.SDG_INTERDEPENDENCIES:
                affected_secondary_sdgs.update(self.SDG_INTERDEPENDENCIES[sdg])
        
        # Remove primary SDGs from secondary set
        affected_secondary_sdgs -= set(primary_sdgs)
        
        # Calculate secondary impacts
        for sdg in affected_secondary_sdgs:
            if sdg not in baseline_indicators:
                continue
                
            baseline = baseline_indicators[sdg]
            indicator_info = SDG_INDICATORS.get(sdg, {})
            lower_is_better = indicator_info.get("lower_is_better", False)
            
            # Secondary impact is smaller
            if lower_is_better:
                change = -baseline * 0.03 * impact_factor
            else:
                change = baseline * 0.02 * impact_factor
            
            final_value = baseline + change
            
            if indicator_info.get("unit") == "%":
                final_value = max(0, min(100, final_value))
            
            secondary[sdg] = {
                "sdg_name": SDG_GOALS[sdg],
                "baseline": round(baseline, 2),
                "final": round(final_value, 2),
                "change": round(change, 2),
                "unit": indicator_info.get("unit", ""),
                "is_secondary": True
            }
        
        return secondary
    
    def _calculate_confidence(
        self,
        scenario_type: str,
        funding_percentage: float,
        timeline_years: int,
        delay_months: int
    ) -> float:
        """Calculate confidence score for the simulation"""
        
        # Base confidence by scenario type
        scenario_confidence = {
            "success": 0.75,
            "partial_success": 0.65,
            "delay": 0.60,
            "failure": 0.70,
            "underfunded": 0.55
        }
        
        base = scenario_confidence.get(scenario_type, 0.5)
        
        # Penalize for long timelines (more uncertainty)
        timeline_penalty = max(0, 0.15 * (timeline_years - 3) / 5.0)
        
        # Penalize for delays
        delay_penalty = min(0.2, delay_months / 60.0)
        
        # Bonus for full funding
        funding_bonus = 0.1 if funding_percentage >= 90 else 0
        
        confidence = base - timeline_penalty - delay_penalty + funding_bonus
        return round(max(0.3, min(0.95, confidence)), 2)
    
    def compare_scenarios(
        self,
        baseline_indicators: Dict[int, float],
        target_sdgs: List[int],
        scenarios: List[str],
        funding_percentage: float,
        timeline_years: int,
        population: int
    ) -> Dict[str, Dict]:
        """Run multiple scenarios and compare results"""
        
        results = {}
        for scenario in scenarios:
            outcomes, affected_pop, confidence = self.simulate_future_impact(
                baseline_indicators=baseline_indicators,
                target_sdgs=target_sdgs,
                scenario_type=scenario,
                funding_percentage=funding_percentage,
                timeline_years=timeline_years,
                population=population
            )
            
            results[scenario] = {
                "outcomes": outcomes,
                "affected_population": affected_pop,
                "confidence": confidence
            }
        
        return results


class AIExplainer:
    """Generate natural language explanations for simulation results"""
    
    @staticmethod
    def generate_explanation(
        scenario_type: str,
        predicted_outcomes: Dict[int, Dict],
        affected_population: int,
        timeline_years: int,
        delay_months: int = 0,
        funding_percentage: float = 100.0
    ) -> Tuple[str, str, str]:
        """
        Generate explanation, policy insight, and risk warning
        
        Returns:
            - explanation: Plain English explanation
            - policy_insight: Policy-level recommendation
            - risk_warning: Warning about risks (if applicable)
        """
        
        # Filter primary SDGs (not secondary effects)
        primary_sdgs = {
            k: v for k, v in predicted_outcomes.items() 
            if not v.get("is_secondary", False)
        }
        
        # Calculate overall impact
        total_change = sum(abs(v["change"]) for v in primary_sdgs.values())
        positive_changes = sum(1 for v in primary_sdgs.values() if v["change"] > 0)
        negative_changes = len(primary_sdgs) - positive_changes
        
        # Build explanation
        scenario_descriptions = {
            "success": "fully succeeds",
            "partial_success": "partially succeeds",
            "delay": "experiences delays",
            "failure": "fails to meet its objectives",
            "underfunded": "receives insufficient funding"
        }
        
        scenario_desc = scenario_descriptions.get(scenario_type, "is implemented")
        
        explanation_parts = []
        
        # Main statement
        if delay_months > 0:
            explanation_parts.append(
                f"If this project {scenario_desc} and is delayed by {delay_months} months over a {timeline_years}-year period:"
            )
        else:
            explanation_parts.append(
                f"If this project {scenario_desc} over a {timeline_years}-year period:"
            )
        
        # Impact on specific SDGs
        for sdg_num, data in list(primary_sdgs.items())[:3]:  # Top 3 SDGs
            change_pct = abs(data["change"] / data["baseline"] * 100) if data["baseline"] != 0 else 0
            direction = "improve" if data["change"] > 0 else "decline"
            
            explanation_parts.append(
                f"• SDG {sdg_num} ({data['sdg_name']}) will {direction} by {abs(data['change']):.1f} {data['unit']} "
                f"({change_pct:.1f}% change)"
            )
        
        # Population impact
        explanation_parts.append(
            f"\nApproximately {affected_population:,} people will be directly affected."
        )
        
        explanation = "\n".join(explanation_parts)
        
        # Policy Insight
        if scenario_type in ["success", "partial_success"]:
            policy_insight = (
                f"Recommended action: Continue supporting this initiative. "
                f"With {funding_percentage:.0f}% funding, {positive_changes} SDG indicators show positive trends. "
                f"Consider scaling the project to reach more communities."
            )
        elif scenario_type == "underfunded":
            policy_insight = (
                f"Critical recommendation: Increase funding from {funding_percentage:.0f}% to at least 80% "
                f"to achieve meaningful impact. Current funding levels may result in incomplete outcomes."
            )
        else:
            policy_insight = (
                f"Risk mitigation needed: Address project challenges immediately. "
                f"Consider reallocating resources or adjusting project scope to salvage partial outcomes."
            )
        
        # Risk Warning
        risk_warning = None
        if negative_changes > 0:
            risk_warning = (
                f"⚠️ Warning: {negative_changes} SDG indicator(s) may experience negative trends. "
                f"Review project design to minimize unintended consequences."
            )
        elif delay_months > 12:
            risk_warning = (
                f"⚠️ Warning: {delay_months}-month delay significantly reduces impact. "
                f"Each additional month of delay further diminishes outcomes and affects {affected_population:,} people."
            )
        elif funding_percentage < 60:
            risk_warning = (
                f"⚠️ Critical: {funding_percentage:.0f}% funding is below minimum viable threshold. "
                f"Project may fail to deliver measurable SDG improvements."
            )
        
        return explanation, policy_insight, risk_warning
