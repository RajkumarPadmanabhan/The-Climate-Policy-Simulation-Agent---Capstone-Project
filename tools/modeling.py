# /tools/modeling.py
# Contains the custom Python logic for the climate simulation model.

from typing import Dict, Any

def run_simplified_climate_model(policy_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates the simplified, interconnected economic and CO2 chain-of-outcomes.
    This function executes the complex calculation requested by the Modeling Agent.
    """
    print(f"--- TOOL: Running Climate Model with rate ${policy_inputs.get('proposed_tax_rate', 'N/A')}...")
    
    proposed_rate = policy_inputs.get('proposed_tax_rate', 0)
    
    # 1. Environmental Effect (CO2 Reduction is proportional to the tax rate)
    co2_reduction_rate = 0.05 + (proposed_rate / 1000.0)
    
    # 2. Economic Effect (GDP Cost is non-linearly proportional to the tax rate)
    gdp_impact = -(proposed_rate ** 1.1) * 0.00005
    
    # 3. Sector Shift Logic
    shift_description = "Minimal shift, requires higher tax."
    if proposed_rate > 60:
         shift_description = "Significant divestment from fossil fuels and strong investment in green hydrogen."
    elif proposed_rate > 30:
         shift_description = "Moderate shift to solar and battery storage investments."

    return {
        "status": "success",
        "simulation_results": {
            "predicted_co2_reduction_percentage": round(co2_reduction_rate * 100, 2),
            "economic_cost_gdp_impact": round(gdp_impact * 100, 3), 
            "energy_sector_shift": shift_description
        }
    }