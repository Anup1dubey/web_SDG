"""
Explainability Layer for SDG Simulations
Generates human-readable explanations for simulation results
"""
from typing import Dict, List, Tuple
import numpy as np
from simulation_core import SimulationState, TimeStepSimulationEngine, ConstraintEngine
from sdg_graph import SDGIndicatorGraph


class SimulationExplainer:
    """
    Analyzes simulation results and generates natural language explanations
    """
    
    def __init__(self, graph: SDGIndicatorGraph, states: List[SimulationState],
                 constraint_engine: ConstraintEngine, target_sdgs: List[int]):
        self.graph = graph
        self.states = states
        self.constraint_engine = constraint_engine
        self.target_sdgs = target_sdgs
    
    def analyze_changes(self) -> Dict[str, Dict]:
        """
        Analyze what changed over the simulation period
        
        Returns:
            Dict of indicator -> {change, pct_change, trend}
        """
        baseline = self.states[0]
        final = self.states[-1]
        
        analysis = {}
        
        for indicator in baseline.indicators.keys():
            baseline_val = baseline.indicators[indicator]
            final_val = final.indicators[indicator]
            
            change = final_val - baseline_val
            pct_change = (change / baseline_val * 100) if baseline_val > 0 else 0
            
            # Determine trend
            if pct_change > 5:
                trend = 'significant_increase'
            elif pct_change > 1:
                trend = 'moderate_increase'
            elif pct_change < -5:
                trend = 'significant_decrease'
            elif pct_change < -1:
                trend = 'moderate_decrease'
            else:
                trend = 'stable'
            
            analysis[indicator] = {
                'baseline': baseline_val,
                'final': final_val,
                'change': change,
                'pct_change': pct_change,
                'trend': trend,
                'indicator_info': self.graph.get_indicator_info(indicator)
            }
        
        return analysis
    
    def identify_top_changes(self, n: int = 5) -> List[Tuple[str, Dict]]:
        """Identify the top N indicators with the most significant changes"""
        analysis = self.analyze_changes()
        
        # Sort by absolute percent change
        sorted_indicators = sorted(
            analysis.items(),
            key=lambda x: abs(x[1]['pct_change']),
            reverse=True
        )
        
        return sorted_indicators[:n]
    
    def identify_bottlenecks(self) -> List[Tuple[str, str]]:
        """
        Identify indicators that didn't improve much despite targeting
        These are likely bottlenecks
        """
        analysis = self.analyze_changes()
        bottlenecks = []
        
        # Check target SDG indicators
        for sdg_num in self.target_sdgs:
            sdg_indicators = self.graph.get_sdg_indicators(sdg_num)
            
            for indicator in sdg_indicators:
                if indicator in analysis:
                    data = analysis[indicator]
                    
                    # If targeted but didn't improve much
                    if data['pct_change'] < 3:  # Less than 3% improvement
                        reason = self._diagnose_bottleneck(indicator, analysis)
                        bottlenecks.append((indicator, reason))
        
        return bottlenecks
    
    def _diagnose_bottleneck(self, indicator: str, analysis: Dict) -> str:
        """Diagnose why an indicator didn't improve"""
        data = analysis[indicator]
        
        # Check if already near maximum
        indicator_info = data['indicator_info']
        if data['final'] > 0.9 * indicator_info['max']:
            return f"Already near maximum capacity ({data['final']:.1f}/{indicator_info['max']:.1f})"
        
        # Check if constrained by other factors
        influences_from = self.graph.get_influences_from(indicator)
        if influences_from:
            # Check if influencing indicators also didn't improve
            weak_supports = []
            for influence in influences_from:
                if influence.target in analysis:
                    if analysis[influence.target]['pct_change'] < 2:
                        weak_supports.append(self.graph.get_indicator_info(influence.target)['name'])
            
            if weak_supports:
                return f"Limited by weak progress in: {', '.join(weak_supports[:2])}"
        
        # Default reason
        effectiveness = self.constraint_engine.get_total_effectiveness()
        if effectiveness < 0.6:
            return f"Constrained by implementation factors ({effectiveness:.0%} effectiveness)"
        
        return "Saturation effects or systemic constraints"
    
    def identify_risk_factors(self) -> List[str]:
        """Identify risks and vulnerabilities in the simulation"""
        analysis = self.analyze_changes()
        risks = []
        
        # Check for negative trends
        for indicator, data in analysis.items():
            if data['trend'] in ['significant_decrease', 'moderate_decrease']:
                indicator_name = data['indicator_info']['name']
                risks.append(f"⚠️ {indicator_name} declined by {abs(data['pct_change']):.1f}% - requires intervention")
        
        # Check for stagnation in critical areas
        critical_indicators = ['health_index', 'poverty_rate', 'water_access', 'food_security']
        for indicator in critical_indicators:
            if indicator in analysis:
                data = analysis[indicator]
                if data['trend'] == 'stable' and indicator in [self.graph.get_sdg_indicators(sdg) for sdg in self.target_sdgs]:
                    risks.append(f"⚠️ {data['indicator_info']['name']} stagnant despite targeting")
        
        # Check for low effectiveness
        effectiveness = self.constraint_engine.get_total_effectiveness()
        if effectiveness < 0.5:
            risks.append(f"⚠️ Overall implementation effectiveness is low ({effectiveness:.0%}) - project may underdeliver")
        
        # Check for delayed effects still pending
        final_state = self.states[-1]
        if len(final_state.delayed_effects) > 0:
            risks.append(f"⏳ {len(final_state.delayed_effects)} delayed effects still pending - full impact not yet realized")
        
        return risks[:5]  # Return top 5 risks
    
    def generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on simulation results"""
        analysis = self.analyze_changes()
        recommendations = []
        
        # Recommend focusing on bottlenecks
        bottlenecks = self.identify_bottlenecks()
        if bottlenecks:
            bottleneck_names = [self.graph.get_indicator_info(b[0])['name'] for b, _ in bottlenecks[:2]]
            recommendations.append(
                f"🎯 Focus additional resources on: {', '.join(bottleneck_names)}"
            )
        
        # Recommend addressing negative trends
        declining = [ind for ind, data in analysis.items() 
                    if data['trend'] in ['significant_decrease', 'moderate_decrease']]
        if declining:
            declining_names = [self.graph.get_indicator_info(d)['name'] for d in declining[:2]]
            recommendations.append(
                f"🚨 Urgent: Address declining trends in {', '.join(declining_names)}"
            )
        
        # Recommend leveraging strong performers
        strong_performers = [(ind, data) for ind, data in analysis.items() 
                            if data['pct_change'] > 10]
        if strong_performers:
            top_performer = strong_performers[0]
            performer_name = top_performer[1]['indicator_info']['name']
            
            # Find what this influences
            influences = self.graph.get_influences_from(top_performer[0])
            if influences:
                target_names = [self.graph.get_indicator_info(inf.target)['name'] for inf in influences[:2]]
                recommendations.append(
                    f"💡 Leverage strong {performer_name} gains to improve {', '.join(target_names)}"
                )
        
        # Recommend constraint mitigation
        effectiveness = self.constraint_engine.get_total_effectiveness()
        if effectiveness < 0.7:
            recommendations.append(
                f"⚙️ Improve implementation conditions - current effectiveness is only {effectiveness:.0%}"
            )
        
        # Recommend longer timeline if needed
        if len(self.states) < 5:
            recommendations.append(
                "📅 Consider extending project timeline for full impact realization"
            )
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def calculate_confidence_score(self) -> float:
        """
        Calculate confidence in the simulation results
        Based on: data quality, constraint severity, feedback loop stability
        """
        confidence = 1.0
        
        # Reduce confidence for severe constraints
        effectiveness = self.constraint_engine.get_total_effectiveness()
        if effectiveness < 0.5:
            confidence *= 0.7
        elif effectiveness < 0.7:
            confidence *= 0.85
        
        # Reduce confidence for high volatility
        analysis = self.analyze_changes()
        volatility_count = sum(1 for data in analysis.values() 
                              if abs(data['pct_change']) > 20)
        if volatility_count > 5:
            confidence *= 0.8
        
        # Reduce confidence for short timelines (less data)
        if len(self.states) < 4:
            confidence *= 0.85
        
        return max(0.5, min(1.0, confidence))
    
    def generate_summary(self) -> Dict:
        """
        Generate a complete summary with human-readable explanations
        """
        analysis = self.analyze_changes()
        top_changes = self.identify_top_changes(5)
        bottlenecks = self.identify_bottlenecks()
        risks = self.identify_risk_factors()
        recommendations = self.generate_recommendations()
        confidence = self.calculate_confidence_score()
        
        # Calculate net SDG progress
        target_indicators = []
        for sdg_num in self.target_sdgs:
            target_indicators.extend(self.graph.get_sdg_indicators(sdg_num))
        
        target_changes = [analysis[ind]['pct_change'] for ind in target_indicators if ind in analysis]
        net_progress = np.mean(target_changes) if target_changes else 0
        
        # Generate narrative summary
        narrative = self._generate_narrative(top_changes, bottlenecks, net_progress)
        
        return {
            'narrative': narrative,
            'net_sdg_progress': net_progress,
            'confidence_score': confidence,
            'top_changes': [
                {
                    'indicator': self.graph.get_indicator_info(ind)['name'],
                    'change': data['change'],
                    'pct_change': data['pct_change'],
                    'baseline': data['baseline'],
                    'final': data['final']
                }
                for ind, data in top_changes
            ],
            'bottlenecks': [
                {
                    'indicator': self.graph.get_indicator_info(ind)['name'],
                    'reason': reason
                }
                for ind, reason in bottlenecks
            ],
            'risks': risks,
            'recommendations': recommendations,
            'effectiveness': self.constraint_engine.get_total_effectiveness()
        }
    
    def _generate_narrative(self, top_changes: List, bottlenecks: List, 
                           net_progress: float) -> str:
        """Generate a natural language narrative of what happened"""
        parts = []
        
        # Opening statement
        if net_progress > 10:
            parts.append(f"The simulation shows strong progress with {net_progress:.1f}% average improvement across target SDGs.")
        elif net_progress > 5:
            parts.append(f"The simulation shows moderate progress with {net_progress:.1f}% average improvement across target SDGs.")
        elif net_progress > 0:
            parts.append(f"The simulation shows limited progress with only {net_progress:.1f}% average improvement across target SDGs.")
        else:
            parts.append(f"The simulation shows concerning results with {abs(net_progress):.1f}% average decline in target SDGs.")
        
        # Top improvements
        if top_changes:
            top_ind, top_data = top_changes[0]
            top_name = self.graph.get_indicator_info(top_ind)['name']
            parts.append(f"{top_name} showed the strongest gains with a {top_data['pct_change']:.1f}% improvement.")
        
        # Bottlenecks
        if bottlenecks:
            bottleneck_ind, reason = bottlenecks[0]
            bottleneck_name = self.graph.get_indicator_info(bottleneck_ind)['name']
            parts.append(f"However, {bottleneck_name} remained a bottleneck - {reason.lower()}.")
        
        # Constraints
        effectiveness = self.constraint_engine.get_total_effectiveness()
        if effectiveness < 0.7:
            parts.append(f"Overall implementation effectiveness was limited to {effectiveness:.0%} due to various constraints.")
        
        return " ".join(parts)
