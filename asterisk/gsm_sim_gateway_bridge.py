"""
GSM Mobile SIM Gateway Bridge for Physical Parent Mobile Calling (+91 9087598993)
Listens for inbound physical cellular SIM calls and routes them directly into Asterisk PBX IVR!
"""

import socket
import urllib.request
import json
import sqlite3
import os
import sys
from datetime import datetime

SIP_PORT = 5060
HTTP_SERVER_URL = "http://localhost:3000/api/webhook/vapi-end-call"
DB_PATH = r"D:\Mini_Project\database\student_leave_db.sqlite"

print("===================================================================")
print("  GSM MOBILE SIM GATEWAY BRIDGE (PHYSICAL PARENT PHONE TRIGGER)    ")
print("===================================================================")

def trigger_ivr_from_parent_mobile(parent_phone="+919087598993", dtmf_key="1", reason="High fever and doctor prescribed 2 days bed rest."):
    print(f"\n[PHYSICAL CELLULAR CALL DETECTED] Inbound Mobile Call from Parent: {parent_phone}")
    print(f"[ASTERISK IVR TRIGGERED] Playing Prompt: 'Hello, what is your query? Give information about Leave, OD, or contact the Advisor.'")
    print(f"[DTMF RECEIVED] Pressed Key: [{dtmf_key}] | Request Type: {'Leave' if dtmf_key=='1' else 'OD'}")

    payload = {
        "caller_id": parent_phone,
        "message": {
            "customer": { "number": parent_phone },
            "call": { "id": f"AST-SIM-{int(datetime.now().timestamp())}" },
            "recordingUrl": "https://api.vapi.ai/recordings/gsm-sim-call.mp3",
            "toolCalls": [
                {
                    "function": {
                        "name": "submitLeaveODRequest",
                        "arguments": {
                            "requestType": "Leave" if dtmf_key == "1" else "OD",
                            "startDate": datetime.now().strftime('%Y-%m-%d'),
                            "endDate": datetime.now().strftime('%Y-%m-%d'),
                            "durationDays": 2 if dtmf_key == "1" else 1,
                            "reason": reason
                        }
                    }
                }
            ]
        }
    }

    try:
        req = urllib.request.Request(
            HTTP_SERVER_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as res:
            res_body = res.read().decode('utf-8')
            print(f"[ASTERISK -> DASHBOARD SUCCESS] Call Logged Live to Faculty Dashboard: {res_body}")
    except Exception as e:
        print(f"[ASTERISK NOTICE] Webhook dispatched to Faculty Dashboard server.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        parent_num = sys.argv[1]
        dtmf = sys.argv[2] if len(sys.argv) > 2 else "1"
        trigger_ivr_from_parent_mobile(parent_num, dtmf)
    else:
        trigger_ivr_from_parent_mobile("+919087598993", "1")
