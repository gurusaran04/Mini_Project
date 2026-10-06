"""
1-Click Automated Vapi Assistant & Webhook Deployment Script
Automatically creates/updates your Vapi AI Assistant with the Server Webhook URL.
"""

import urllib.request
import json
import os

print("===================================================================")
print("  🚀 AUTOMATED VAPI AI ASSISTANT & SERVER WEBHOOK DEPLOYER         ")
print("===================================================================")

VAPI_API_KEY = input("\n🔑 Enter your Vapi Private API Key (from https://dashboard.vapi.ai/account): ").strip()

if not VAPI_API_KEY:
    print("❌ Error: Vapi API Key is required.")
    exit(1)

WEBHOOK_URL = "https://profound-senior-engaging.ngrok-free.dev/api/webhook/vapi-end-call"

assistant_payload = {
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
                "content": "You are Aura, the official AI Voice Assistant for St. Jude Tech Affairs. Ask for the student leave/OD reason, duration, dates, and submit."
            }
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "submitLeaveODRequest",
                    "description": "Submits a student leave or On-Duty (OD) request.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "requestType": {"type": "string", "enum": ["Leave", "OD"]},
                            "startDate": {"type": "string"},
                            "endDate": {"type": "string"},
                            "durationDays": {"type": "integer"},
                            "reason": {"type": "string"}
                        },
                        "required": ["requestType", "startDate", "endDate", "durationDays", "reason"]
                    }
                }
            }
        ]
    },
    "voice": {
        "provider": "playht",
        "voiceId": "jennifer"
    },
    "serverUrl": WEBHOOK_URL
}

try:
    req = urllib.request.Request(
        "https://api.vapi.ai/assistant",
        data=json.dumps(assistant_payload).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {VAPI_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        print("\n✅ SUCCESS: Assistant Created and Bound to Webhook!")
        print(f"📌 Assistant ID: {res_data.get('id')}")
        print(f"🔗 Server URL set to: {res_data.get('serverUrl')}")
except Exception as e:
    print(f"\n❌ Error deploying assistant to Vapi API: {e}")
