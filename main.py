# main.py
# The primary entry point for the ECHO Agent system.

from agents.definitions import echo_root_agent, POLICY_DATABASE # Import orchestrator and global state

if __name__ == "__main__":
    print("--- Running ECHO Agent System (main.py) ---")

    # High-impact user prompt for the capstone project
    policy_proposal = "Analyze the effect of a $120 per ton carbon tax on all non-renewable energy sectors for the next 5 years."
    analyst_email = "jane.doe@thinktank.com"
    
    print(f"\n*** USER INPUT: {policy_proposal} ***")
    
    # Execute the full multi-agent chain (RootAgent orchestrates all sub-agents)
    final_orchestration_summary = echo_root_agent.run(policy_proposal, analyst_email)
    
    print("\n" + "="*80)
    print("DEMONSTRATING CRUD (Reading the saved data):")
    
    # Read back saved data to show successful persistence
    print(f"\nPolicy Database Contents (Total Records: {len(POLICY_DATABASE)}):")
    for policy_id, record in POLICY_DATABASE.items():
        print(f"  ID: {policy_id}")
        # Accessing the nested summary created by the Synthesis Agent
        print(f"  Summary: {record['summary']['co2_reduction']} CO2 Reduction, {record['summary']['economic_impact']} Economic Impact")
        print("-" * 20)