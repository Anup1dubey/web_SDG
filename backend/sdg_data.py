"""
Mock SDG data and baseline indicators
"""

# 17 Sustainable Development Goals
SDG_GOALS = {
    1: "No Poverty",
    2: "Zero Hunger",
    3: "Good Health and Well-being",
    4: "Quality Education",
    5: "Gender Equality",
    6: "Clean Water and Sanitation",
    7: "Affordable and Clean Energy",
    8: "Decent Work and Economic Growth",
    9: "Industry, Innovation and Infrastructure",
    10: "Reduced Inequalities",
    11: "Sustainable Cities and Communities",
    12: "Responsible Consumption and Production",
    13: "Climate Action",
    14: "Life Below Water",
    15: "Life on Land",
    16: "Peace, Justice and Strong Institutions",
    17: "Partnerships for the Goals"
}

# Key indicators for each SDG (simplified for demo)
SDG_INDICATORS = {
    1: {
        "code": "SDG1.1",
        "name": "Population below poverty line",
        "unit": "%",
        "lower_is_better": True
    },
    2: {
        "code": "SDG2.1",
        "name": "Prevalence of undernourishment",
        "unit": "%",
        "lower_is_better": True
    },
    3: {
        "code": "SDG3.1",
        "name": "Life expectancy at birth",
        "unit": "years",
        "lower_is_better": False
    },
    4: {
        "code": "SDG4.1",
        "name": "Primary education completion rate",
        "unit": "%",
        "lower_is_better": False
    },
    5: {
        "code": "SDG5.1",
        "name": "Gender wage gap",
        "unit": "%",
        "lower_is_better": True
    },
    6: {
        "code": "SDG6.1",
        "name": "Access to clean water",
        "unit": "%",
        "lower_is_better": False
    },
    7: {
        "code": "SDG7.1",
        "name": "Access to electricity",
        "unit": "%",
        "lower_is_better": False
    },
    8: {
        "code": "SDG8.1",
        "name": "Unemployment rate",
        "unit": "%",
        "lower_is_better": True
    },
    9: {
        "code": "SDG9.1",
        "name": "Internet access rate",
        "unit": "%",
        "lower_is_better": False
    },
    10: {
        "code": "SDG10.1",
        "name": "Income inequality (Gini coefficient)",
        "unit": "index",
        "lower_is_better": True
    },
    11: {
        "code": "SDG11.1",
        "name": "Urban air quality (PM2.5)",
        "unit": "μg/m³",
        "lower_is_better": True
    },
    12: {
        "code": "SDG12.1",
        "name": "Waste recycling rate",
        "unit": "%",
        "lower_is_better": False
    },
    13: {
        "code": "SDG13.1",
        "name": "CO2 emissions per capita",
        "unit": "tons",
        "lower_is_better": True
    },
    14: {
        "code": "SDG14.1",
        "name": "Ocean plastic pollution",
        "unit": "tons/year",
        "lower_is_better": True
    },
    15: {
        "code": "SDG15.1",
        "name": "Forest coverage",
        "unit": "%",
        "lower_is_better": False
    },
    16: {
        "code": "SDG16.1",
        "name": "Crime rate",
        "unit": "per 100k",
        "lower_is_better": True
    },
    17: {
        "code": "SDG17.1",
        "name": "Development aid received",
        "unit": "million USD",
        "lower_is_better": False
    }
}

# Sample baseline values for different region types
BASELINE_TEMPLATES = {
    "developing_urban": {
        1: 22.5, 2: 18.3, 3: 68.5, 4: 72.0, 5: 23.0,
        6: 65.0, 7: 78.0, 8: 12.5, 9: 45.0, 10: 0.42,
        11: 45.0, 12: 15.0, 13: 4.2, 14: 850.0, 15: 28.0,
        16: 125.0, 17: 50.0
    },
    "developed_urban": {
        1: 8.5, 2: 5.2, 3: 79.5, 4: 95.0, 5: 12.0,
        6: 98.0, 7: 99.5, 8: 5.5, 9: 88.0, 10: 0.32,
        11: 18.0, 12: 42.0, 13: 7.8, 14: 320.0, 15: 38.0,
        16: 45.0, 17: 5.0
    },
    "rural": {
        1: 35.0, 2: 28.5, 3: 62.0, 4: 58.0, 5: 28.0,
        6: 48.0, 7: 52.0, 8: 18.0, 9: 25.0, 10: 0.48,
        11: 55.0, 12: 8.0, 13: 2.5, 14: 500.0, 15: 45.0,
        16: 85.0, 17: 75.0
    }
}

def get_baseline_for_region(region_type="developing_urban"):
    """Get baseline SDG values for a region type"""
    return BASELINE_TEMPLATES.get(region_type, BASELINE_TEMPLATES["developing_urban"])
