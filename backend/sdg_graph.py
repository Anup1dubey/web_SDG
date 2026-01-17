"""
SDG Indicator Graph System
Models interdependencies, delays, and influence weights between SDG indicators
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np


@dataclass
class IndicatorInfluence:
    """Represents how one indicator influences another"""
    target: str
    weight: float  # Positive or negative influence strength
    delay_years: int  # How long before effect is felt
    description: str


class SDGIndicatorGraph:
    """
    Models SDG indicators as a directed weighted graph
    Each indicator can influence others with time delays
    """
    
    def __init__(self):
        self.indicators = self._initialize_indicators()
        self.influences = self._initialize_influences()
        
    def _initialize_indicators(self) -> Dict[str, Dict]:
        """Initialize baseline SDG indicators with their properties"""
        return {
            # SDG 1: No Poverty
            'poverty_rate': {
                'name': 'Poverty Rate',
                'baseline': 20.0,  # percentage
                'min': 0.0,
                'max': 100.0,
                'unit': '%',
                'sdg': 1
            },
            
            # SDG 2: Zero Hunger
            'food_security': {
                'name': 'Food Security Index',
                'baseline': 65.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 2
            },
            
            # SDG 3: Good Health
            'health_index': {
                'name': 'Health Access Index',
                'baseline': 70.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 3
            },
            
            # SDG 4: Quality Education
            'education_index': {
                'name': 'Education Quality Index',
                'baseline': 68.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 4
            },
            
            # SDG 5: Gender Equality
            'gender_equality': {
                'name': 'Gender Equality Index',
                'baseline': 72.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 5
            },
            
            # SDG 6: Clean Water
            'water_access': {
                'name': 'Clean Water Access',
                'baseline': 75.0,
                'min': 0.0,
                'max': 100.0,
                'unit': '%',
                'sdg': 6
            },
            
            # SDG 7: Clean Energy
            'clean_energy': {
                'name': 'Clean Energy Share',
                'baseline': 30.0,
                'min': 0.0,
                'max': 100.0,
                'unit': '%',
                'sdg': 7
            },
            
            # SDG 8: Decent Work
            'employment_rate': {
                'name': 'Employment Rate',
                'baseline': 65.0,
                'min': 0.0,
                'max': 100.0,
                'unit': '%',
                'sdg': 8
            },
            
            # SDG 9: Industry & Innovation
            'innovation_index': {
                'name': 'Innovation Index',
                'baseline': 55.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 9
            },
            
            # SDG 10: Reduced Inequalities
            'equality_index': {
                'name': 'Equality Index',
                'baseline': 60.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 10
            },
            
            # SDG 11: Sustainable Cities
            'urban_sustainability': {
                'name': 'Urban Sustainability Index',
                'baseline': 58.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 11
            },
            
            # SDG 12: Responsible Consumption
            'circular_economy': {
                'name': 'Circular Economy Index',
                'baseline': 40.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 12
            },
            
            # SDG 13: Climate Action
            'emissions_reduction': {
                'name': 'Emissions Reduction',
                'baseline': 35.0,
                'min': 0.0,
                'max': 100.0,
                'unit': '%',
                'sdg': 13
            },
            
            # SDG 14: Life Below Water
            'marine_health': {
                'name': 'Marine Ecosystem Health',
                'baseline': 62.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 14
            },
            
            # SDG 15: Life On Land
            'terrestrial_health': {
                'name': 'Terrestrial Ecosystem Health',
                'baseline': 68.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 15
            },
            
            # SDG 16: Peace & Justice
            'governance_index': {
                'name': 'Governance Quality Index',
                'baseline': 64.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 16
            },
            
            # SDG 17: Partnerships
            'partnership_index': {
                'name': 'Partnership Effectiveness',
                'baseline': 60.0,
                'min': 0.0,
                'max': 100.0,
                'unit': 'index',
                'sdg': 17
            }
        }
    
    def _initialize_influences(self) -> Dict[str, List[IndicatorInfluence]]:
        """
        Define how indicators influence each other
        Format: source_indicator -> [list of influences on other indicators]
        """
        return {
            'education_index': [
                IndicatorInfluence('employment_rate', 0.5, 1, 'Education improves job prospects with 1-year delay'),
                IndicatorInfluence('health_index', 0.3, 2, 'Education leads to better health behaviors'),
                IndicatorInfluence('poverty_rate', -0.4, 2, 'Education reduces poverty over time'),
                IndicatorInfluence('innovation_index', 0.6, 1, 'Education drives innovation'),
            ],
            
            'employment_rate': [
                IndicatorInfluence('poverty_rate', -0.7, 0, 'Employment directly reduces poverty'),
                IndicatorInfluence('health_index', 0.3, 1, 'Employment improves health access'),
                IndicatorInfluence('food_security', 0.4, 0, 'Employment enables food access'),
                IndicatorInfluence('equality_index', 0.2, 1, 'Employment reduces inequality'),
            ],
            
            'health_index': [
                IndicatorInfluence('employment_rate', 0.3, 1, 'Health enables workforce participation'),
                IndicatorInfluence('poverty_rate', -0.3, 1, 'Health reduces poverty through productivity'),
                IndicatorInfluence('education_index', 0.2, 2, 'Health enables education participation'),
            ],
            
            'water_access': [
                IndicatorInfluence('health_index', 0.5, 0, 'Clean water immediately improves health'),
                IndicatorInfluence('food_security', 0.3, 1, 'Water access enables agriculture'),
                IndicatorInfluence('employment_rate', 0.2, 1, 'Water access enables economic activity'),
            ],
            
            'clean_energy': [
                IndicatorInfluence('emissions_reduction', 0.8, 0, 'Clean energy directly reduces emissions'),
                IndicatorInfluence('health_index', 0.3, 1, 'Clean energy reduces pollution-related illness'),
                IndicatorInfluence('innovation_index', 0.4, 1, 'Clean energy drives tech innovation'),
            ],
            
            'circular_economy': [
                IndicatorInfluence('emissions_reduction', 0.5, 1, 'Circular economy reduces waste emissions'),
                IndicatorInfluence('employment_rate', 0.3, 1, 'Circular economy creates green jobs'),
                IndicatorInfluence('marine_health', 0.3, 2, 'Reduced waste improves ocean health'),
                IndicatorInfluence('terrestrial_health', 0.3, 2, 'Reduced waste improves land health'),
            ],
            
            'emissions_reduction': [
                IndicatorInfluence('health_index', 0.4, 2, 'Lower emissions improve respiratory health'),
                IndicatorInfluence('marine_health', 0.5, 3, 'Lower emissions slow ocean acidification'),
                IndicatorInfluence('terrestrial_health', 0.5, 3, 'Lower emissions preserve ecosystems'),
            ],
            
            'innovation_index': [
                IndicatorInfluence('employment_rate', 0.4, 1, 'Innovation creates new jobs'),
                IndicatorInfluence('clean_energy', 0.6, 2, 'Innovation enables clean energy transition'),
                IndicatorInfluence('circular_economy', 0.5, 2, 'Innovation enables circular models'),
            ],
            
            'governance_index': [
                IndicatorInfluence('equality_index', 0.5, 1, 'Good governance reduces inequality'),
                IndicatorInfluence('partnership_index', 0.6, 1, 'Good governance enables partnerships'),
                IndicatorInfluence('education_index', 0.3, 2, 'Good governance improves education systems'),
            ],
            
            'gender_equality': [
                IndicatorInfluence('employment_rate', 0.4, 1, 'Gender equality increases labor participation'),
                IndicatorInfluence('education_index', 0.3, 1, 'Gender equality improves education access'),
                IndicatorInfluence('poverty_rate', -0.3, 2, 'Gender equality reduces household poverty'),
            ],
            
            'urban_sustainability': [
                IndicatorInfluence('health_index', 0.3, 1, 'Sustainable cities improve health'),
                IndicatorInfluence('emissions_reduction', 0.4, 1, 'Sustainable cities reduce emissions'),
                IndicatorInfluence('equality_index', 0.2, 2, 'Sustainable cities reduce urban inequality'),
            ],
        }
    
    def get_influences_from(self, indicator: str) -> List[IndicatorInfluence]:
        """Get all indicators influenced by the given indicator"""
        return self.influences.get(indicator, [])
    
    def get_indicator_info(self, indicator: str) -> Dict:
        """Get information about an indicator"""
        return self.indicators.get(indicator, {})
    
    def get_all_indicators(self) -> List[str]:
        """Get list of all indicator keys"""
        return list(self.indicators.keys())
    
    def get_sdg_indicators(self, sdg_number: int) -> List[str]:
        """Get all indicators related to a specific SDG"""
        return [
            key for key, info in self.indicators.items()
            if info.get('sdg') == sdg_number
        ]
