#!/usr/bin/env python3
"""
Asterisk Gateway Interface (AGI) Python Handler Script
Transmits incoming Asterisk IVR call parameters to the Faculty Dashboard server.
"""

import sys
import urllib.request
import json
from datetime import datetime

# Parse Arguments passed from Asterisk extensions.conf:
# sys.argv[1] = CALLERID(num)
# sys.argv[2] = Request Type (Leave or OD)
# sys.argv[3] = Reason text

caller_id = sys.argv[1] if len(sys.argv) > 1 else "+15559876543"
req_type = sys.argv[2] if len(sys.argv) > 2 else "Leave"
reason_text = sys.argv[3] if len(sys.argv) > 3 else "Voice submission via Asterisk PBX"

SERVER_URL = "http://localhost:3000/api/webhook/vapi-end-call"

today_str = datetime.now().strftime('%Y-%m-%d')

payload = {
    "message": {
        "customer": { "number": caller_id },
        "call": { "id": f"AST-{int(datetime.now().timestamp())}" },
        "recordingUrl": "https://api.vapi.ai/recordings/asterisk-sample.mp3",
        "toolCalls": [
            {
                "function": {
                    "name": "submitLeaveODRequest",
                    "arguments": {
                        "requestType": req_type,
                        "startDate": today_str,
                        "endDate": today_str,
                        "durationDays": 1,
                        "reason": reason_text
                    }
                }
            }
        ]
    }
}

try:
    req = urllib.request.Request(
        SERVER_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as res:
        response_text = res.read().decode('utf-8')
        print(f"VERBOSE \"Asterisk AGI Response: {response_text}\" 1")
except Exception as e:
    print(f"VERBOSE \"Asterisk AGI Error: {e}\" 1")
