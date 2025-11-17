# /tools/notifications.py
# Contains the functions for sending alerts and external notifications.

from typing import Dict, Any

def send_policy_alert(payload: Dict[str, Any]) -> str:
    """Simulates sending an external notification (email and in-app alert)."""
    recipient = payload.get("recipient", "analyst@globalclimate.org")
    policy_text = payload.get("policy_text", "N/A Policy")
    
    # 1. Simulate Email Notification
    email_status = f"EMAIL SENT to {recipient}. Subject: Policy Analysis Complete for '{policy_text[:30]}...'"
    
    # 2. Simulate In-App Alert (Visible in console log)
    alert_status = f"ALERT GENERATED: Policy '{policy_text[:30]}...' analysis is ready for review."

    print("\n" + "*"*50)
    print(f"| {email_status}")
    print(f"| {alert_status}")
    print("*"*50 + "\n")
    
    return f"NOTIFICATION SUCCESS: Email and in-app alert dispatched."