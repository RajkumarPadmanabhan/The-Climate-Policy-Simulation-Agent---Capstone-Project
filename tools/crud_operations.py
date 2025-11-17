# /tools/crud_operations.py
# Contains the simulated database and CRUD management functions.

import uuid
from typing import Dict, Any

# Simulated persistent storage for policy records
POLICY_DATABASE: Dict[str, Dict[str, Any]] = {}

def policy_db_manager(payload: Dict[str, Any]) -> str:
    """Performs CRUD operations on the simulated policy database."""
    global POLICY_DATABASE
    action = payload.get("action", "CREATE")
    data = payload.get("report_data", {})
    policy_id = payload.get("policy_id")

    if action == "CREATE":
        if not data:
            return "CRUD ERROR: No data provided for creation."
        
        new_id = str(uuid.uuid4())
        # Save the full structured summary
        POLICY_DATABASE[new_id] = {"summary": data} 
        print(f"CRUD SUCCESS: Policy created with ID: {new_id} and saved.")
        return f"CRUD SUCCESS: Policy '{data.get('policy_text', 'N/A')}' created with ID: {new_id}."
    
    elif action == "READ" and policy_id:
        record = POLICY_DATABASE.get(policy_id, {"status": "error", "message": "Policy not found."})
        return f"CRUD READ: Record for {policy_id}: {record}"

    elif action == "UPDATE" and policy_id:
        if policy_id in POLICY_DATABASE:
            POLICY_DATABASE[policy_id]['summary'].update(data)
            return f"CRUD SUCCESS: Policy {policy_id} updated."
        return f"CRUD ERROR: Policy {policy_id} not found for update."
        
    elif action == "DELETE" and policy_id:
        if policy_id in POLICY_DATABASE:
            del POLICY_DATABASE[policy_id]
            return f"CRUD SUCCESS: Policy {policy_id} deleted."
        return f"CRUD ERROR: Policy {policy_id} not found for deletion."
    
    return f"CRUD ERROR: Invalid action or missing ID for action: {action}"