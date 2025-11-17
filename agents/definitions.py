# /agents/definitions.py
# Defines the specialized agents and the main orchestration flow.

from typing import Dict, Any
from .core_components import Agent, Tool, RootAgent
from tools.modeling import run_simplified_climate_model
from tools.crud_operations import policy_db_manager, POLICY_DATABASE # Note: POLICY_DATABASE is referenced here
from tools.notifications import send_policy_alert

# --- Tool Definitions (Wrapping the external functions) ---
modeling_tool = Tool(
    name="run_simplified_climate_model",
    func=run_simplified_climate_model,
    description="Runs a simplified, integrated climate and economic model to forecast policy impacts."
)
policy_db_tool = Tool(
    name="PolicyDBTool",
    func=policy_db_manager,
    description="Manages policy records (CREATE, READ, UPDATE, DELETE) in the persistent database."
)
notification_tool = Tool(
    name="NotificationTool",
    func=send_policy_alert,
    description="Sends email and in-app alerts to users upon analysis completion."
)
google_search_tool_mock = Tool(
    name="GoogleSearchTool_Mock",
    func=lambda x: x,
    description="Searches the web for real-time market data."
)

# --- Agent Definitions ---

# 1. Data Retrieval Agent (Uses Mock Google Search Tool)
data_retrieval_agent = Agent(
    name="Data_Retrieval_Agent",
    instruction="Use Google Search Tool to find current market data required for modeling. Format output as JSON.",
    tools=[google_search_tool_mock]
)

# 2. Modeling Agent (Uses Custom Python Modeling Tool)
modeling_agent = Agent(
    name="Modeling_Agent",
    instruction="Execute the 'run_simplified_climate_model' tool using inputs from the Data Retrieval Agent. Pass raw simulation results.",
    tools=[modeling_tool]
)

# 3. Synthesis Agent (Pure reasoning and formatting)
synthesis_agent = Agent(
    name="Synthesis_Agent",
    model="gemini-2.5-pro-preview-09-2025",
    instruction="Analyze the raw simulation output and policy proposal to create a structured JSON summary ready for persistence.",
    tools=[]
)

# 4. Persistence Agent (Uses CRUD and Notification Tools)
persistence_agent = Agent(
    name="Persistence_Agent",
    instruction="Receive the final structured report. First, use PolicyDBTool to CREATE a new record. Second, use NotificationTool to send an alert to the recipient.",
    tools=[policy_db_tool, notification_tool]
)

# --- Root Agent (Orchestrator) ---
echo_root_agent = RootAgent(
    name="ECHO_Root_Agent",
    instruction="Analyze a climate policy by gathering data, modeling impacts, generating a report summary, and persisting the result with a notification.",
    sub_agents=[data_retrieval_agent, modeling_agent, synthesis_agent, persistence_agent]
)

# Expose POLICY_DATABASE globally for main.py to inspect results
__all__ = ['echo_root_agent', 'POLICY_DATABASE']