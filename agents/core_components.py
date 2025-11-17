# /agents/core_components.py
# Contains foundational classes and mock helper methods for the agent system.

import json
from typing import Dict, Any, List
from tools.crud_operations import POLICY_DATABASE # Import the global database reference

class Tool:
    """Represents an ADK Tool (a wrapped function)."""
    def __init__(self, name: str, func, description: str):
        self.name = name
        self.func = func
        self.description = description

class Agent:
    """Represents a specialized sub-agent."""
    def __init__(self, name: str, instruction: str, tools: List[Tool] = None, model: str = "gemini-2.5-flash"):
        self.name = name
        self.instruction = instruction
        self.tools = tools if tools is not None else []
        self.model = model

    def run(self, input_data: str) -> str:
        """Simulates the agent's LLM-driven execution."""
        print(f"\n[{self.name}] received input: {input_data[:75]}...")

        if self.tools:
            tool = self.tools[0]
            print(f"[{self.name}] -> Deciding to use Tool: {tool.name}")
            
            if tool.name == "GoogleSearchTool_Mock":
                return self._mock_data_retrieval(input_data)
            
            # Runs external tools defined in the /tools/ folder
            elif tool.name in ["PolicyDBTool", "NotificationTool", "run_simplified_climate_model"]:
                try:
                    parsed_inputs = json.loads(input_data)
                    return json.dumps(tool.func(parsed_inputs))
                except json.JSONDecodeError:
                    return json.dumps({"status": "error", "message": "Invalid JSON input."})
        
        return self._mock_synthesis(input_data)

    def _mock_data_retrieval(self, policy_text: str) -> str:
        """Mocks the Data Retrieval Agent finding data via search and structuring the output."""
        print(f"[{self.name}] -> Performing Mock Google Search for current data...")
        proposed_tax_rate = 50.0 
        if "carbon tax" in policy_text:
            try:
                parts = policy_text.split('$')
                if len(parts) > 1:
                    rate_str = parts[1].split()[0]
                    proposed_tax_rate = float(rate_str)
            except ValueError:
                pass 

        return json.dumps({
            "status": "success",
            "policy_text": policy_text,
            "proposed_tax_rate": proposed_tax_rate,
            "real_time_carbon_price": 82.35,
            "current_energy_mix": {"fossil": 0.62, "renewable": 0.38},
            "economic_forecast_stability": "high"
        })

    def _mock_synthesis(self, model_output: str) -> str:
        """Mocks the Synthesis Agent generating a structured JSON summary."""
        print(f"[{self.name}] -> Synthesizing comprehensive policy report...")
        try:
            data = json.loads(model_output)
            results = data['simulation_results']
            
            summary = {
                "policy_text": data.get('policy_text', 'N/A'),
                "co2_reduction": f"{results['predicted_co2_reduction_percentage']}%",
                "economic_impact": f"{results['economic_cost_gdp_impact']}% GDP change",
                "sector_shift": results['energy_sector_shift'],
                "risk_rating": "Low" if results['economic_cost_gdp_impact'] > -0.01 else "Moderate"
            }
            
            return json.dumps({"status": "ready_to_save", "summary": summary, "policy_text": summary["policy_text"]})
            
        except Exception as e:
            return json.dumps({"status": "error", "message": f"Error synthesizing report: {e}"})

class RootAgent:
    """Represents the main orchestrator."""
    def __init__(self, name: str, instruction: str, sub_agents: List[Agent]):
        self.name = name
        self.instruction = instruction
        self.sub_agents = sub_agents

    def run(self, user_prompt: str, recipient_email: str) -> str:
        """Executes the 4-stage multi-agent chain."""
        print(f"\n--- Root Agent: {self.name} START (Email: {recipient_email}) ---")

        # 1. Data Retrieval Agent
        current_data_str = self.sub_agents[0].run(user_prompt)
        
        # 2. Modeling Agent
        model_output_str = self.sub_agents[1].run(current_data_str)
        
        # 3. Synthesis Agent
        synthesis_input = {
            "policy_text": user_prompt, 
            "simulation_results": json.loads(model_output_str).get('simulation_results', {})
        }
        synthesis_output_str = self.sub_agents[2].run(json.dumps(synthesis_input))
        
        # 4. Persistence Agent
        persistence_input = {
            "report_data": json.loads(synthesis_output_str).get('summary', {}),
            "recipient": recipient_email,
            "policy_text": user_prompt 
        }
        final_action_str = self.sub_agents[3].run(json.dumps(persistence_input))
        
        print(f"\n--- Root Agent: {self.name} END ---")
        return final_action_str