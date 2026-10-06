"""
Vapi AI Cloud Telephony Webhook Binding Script
Configures live Vapi Virtual Number webhook endpoint to route incoming phone calls to your Faculty Dashboard.
"""

import urllib.request
import json

# Your live server endpoint
SERVER_WEBHOOK_URL = "http://localhost:3000/api/webhook/vapi-end-call"

print("===============================================================")
print("  AURA IVR - LIVE CLOUD TELEPHONY VAPI BINDING CONFIGURATION   ")
print("===============================================================")
print(f"✅ Webhook Server URL: {SERVER_WEBHOOK_URL}")

vapi_assistant_payload = {
    "name": "Aura College Voice IVR Assistant",
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-2",
        "language": "en"
    },
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "You are Aura, the official AI Voice Assistant for St. Jude Tech Affairs. Verify the parent, take their leave/OD request details, and submit."
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "submitLeaveODRequest",
                    "description": "Submits a leave or On-Duty (OD) request for a student ward.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requestType": {"type": "string", "enum": ["Leave", "OD"]},
                            "startDate": {"type": "string", "description": "Start date in YYYY-MM-DD"},
                            "endDate": {"type": "string", "description": "End date in YYYY-MM-DD"},
                            "durationDays": {"type": "integer", "description": "Number of days"},
                            "reason": {"type": "string", "description": "Detailed reason for absence"}
                        },
                        "required": ["requestType", "startDate", "endDate", "durationDays", "reason"]
                    }
                }
            }
        ]
    },
    "serverUrl": SERVER_WEBHOOK_URL
}

print("\n📋 Paste this Configuration into your Vapi.ai / Twilio Assistant Settings:")
print("---------------------------------------------------------------")
print(json.dumps(vapi_assistant_payload, indent=2))
print("---------------------------------------------------------------")
