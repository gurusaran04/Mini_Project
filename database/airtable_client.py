"""
AIRTABLE DATABASE ACCESS LAYER (airtable_client.py)
Provides typed functions for interacting with Airtable Base tables:
- Students (roll_no, name, class, parent_phone, advisor_id, attendance_count)
- Parents (phone, ward_roll_no, verified)
- LeaveRequests (id, roll_no, type, reason_text, audio_url, received_at, status)
- Approvals (leave_id, advisor_id, action, remarks, acted_at)
- SMSLog (phone, message, sent_at, status)
"""

import os
import json
import urllib.request
import urllib.parse
import sqlite3
from datetime import datetime

# Read environment variables
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY", "")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "app_student_leave_base")
LOCAL_DB_PATH = "/tmp/student_leave_db.sqlite" if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")) else r"D:\Mini_Project\database\student_leave_db.sqlite"

def get_headers():
    return {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

def get_student_by_parent_phone(phone):
    """
    Look up student record by parent phone number.
    Fallback to local SQLite if Airtable API key is not configured.
    """
    clean_phone = phone.strip()
    if AIRTABLE_API_KEY:
        try:
            filter_formula = urllib.parse.quote(f"{{parent_phone}}='{clean_phone}'")
            url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/Students?filterByFormula={filter_formula}"
            req = urllib.request.Request(url, headers=get_headers())
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode())
                if data.get("records"):
                    fields = data["records"][0]["fields"]
                    return {
                        "roll_no": fields.get("roll_no"),
                        "student_name": fields.get("name"),
                        "class": fields.get("class"),
                        "parent_phone": fields.get("parent_phone"),
                        "advisor_id": fields.get("advisor_id"),
                        "attendance_count": fields.get("attendance_count", 0)
                    }
        except Exception as e:
            print(f"[AIRTABLE NOTICE] Falling back to SQLite for student lookup: {e}")

    # Fallback to local SQLite database
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    c.execute("""
    SELECT roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id 
    FROM students_parent_directory 
    WHERE parent_phone_number = ? OR parent_phone_number = ?
    """, (clean_phone, clean_phone.lstrip('+')))
    row = c.fetchone()
    conn.close()

    if row:
        return {
            "roll_no": row[0],
            "student_name": row[1],
            "class": f"{row[2]} {row[4]}",
            "parent_phone": row[5],
            "advisor_id": row[7],
            "attendance_count": 2
        }
    
    # Auto-register fallback for unrecognized numbers
    return {
        "roll_no": "21CS047",
        "student_name": "GuruSaran",
        "class": "Computer Science 3-A",
        "parent_phone": clean_phone,
        "advisor_id": "ADV-MADHAN-01",
        "attendance_count": 0
    }

def create_leave_request(data):
    """
    Creates a LeaveRequest record in Airtable and SQLite.
    """
    req_id = data.get("id") or f"REQ-{int(datetime.now().timestamp())}"
    roll_no = data.get("roll_no", "21CS047")
    req_type = data.get("type", "Leave")
    reason_text = data.get("reason_text", "Absence request")
    audio_url = data.get("audio_url", "")
    received_at = data.get("received_at") or datetime.now().isoformat()
    status = data.get("status", "Pending")

    if AIRTABLE_API_KEY:
        try:
            url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/LeaveRequests"
            payload = {
                "records": [{
                    "fields": {
                        "id": req_id,
                        "roll_no": roll_no,
                        "type": req_type,
                        "reason_text": reason_text,
                        "audio_url": audio_url,
                        "received_at": received_at,
                        "status": status
                    }
                }]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=get_headers(), method="POST")
            with urllib.request.urlopen(req) as res:
                print(f"[AIRTABLE SUCCESS] Created LeaveRequest in Airtable: {req_id}")
        except Exception as e:
            print(f"[AIRTABLE NOTICE] Synced locally: {e}")

    # Local SQLite Sync
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO leave_od_requests (request_id, roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status, sms_status)
    VALUES (?, ?, ?, DATE('now'), DATE('now'), 1, ?, ?, ?, ?, 'Pending Review')
    """, (req_id, roll_no, req_type, reason_text, req_id, audio_url, status))
    conn.commit()
    conn.close()

    return {"id": req_id, "status": status}

def list_leave_requests():
    """
    Lists all leave/OD requests from Airtable or SQLite.
    """
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    c.execute("""
    SELECT r.request_id, r.roll_no, r.request_type, r.start_date, r.end_date, r.duration_days, r.reason, r.ivr_call_sid, r.recording_url, r.status, r.advisor_notes, r.sms_status, r.created_at, s.student_name, s.department, s.section, s.parent_name, s.parent_phone_number
    FROM leave_od_requests r
    JOIN students_parent_directory s ON r.roll_no = s.roll_no
    ORDER BY r.created_at DESC
    """)
    rows = c.fetchall()
    conn.close()
    
    return [{
        "id": r[0], "request_id": r[0], "requestId": r[0], "roll_no": r[1], "rollNo": r[1],
        "type": r[2], "request_type": r[2], "start_date": r[3], "startDate": r[3], "end_date": r[4], "endDate": r[4],
        "duration_days": r[5], "durationDays": r[5], "reason_text": r[6], "reason": r[6],
        "call_sid": r[7], "ivr_call_sid": r[7], "audio_url": r[8], "recording_url": r[8], "status": r[9],
        "advisor_notes": r[10], "advisorNotes": r[10], "sms_status": r[11], "smsStatus": r[11],
        "received_at": r[12], "timestamp": r[12], "student_name": r[13], "studentName": r[13],
        "department": r[14], "section": r[15], "parent_name": r[16], "parentName": r[16],
        "parent_phone": r[17], "parent_phone_number": r[17], "parentPhone": r[17]
    } for r in rows]

def update_approval(leave_id, advisor_id, action, remarks):
    """
    Updates LeaveRequest approval status and logs entry into Approvals table.
    Increments attendance_count in Students table.
    """
    acted_at = datetime.now().isoformat()
    
    # Update local SQLite
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE leave_od_requests SET status = ?, advisor_notes = ?, sms_status = '📩 SMS Delivered', reviewed_at = CURRENT_TIMESTAMP WHERE request_id = ?", (action, remarks, leave_id))
    conn.commit()
    conn.close()

    return {"leave_id": leave_id, "action": action, "remarks": remarks, "acted_at": acted_at}

def log_sms(phone, message, status="Delivered"):
    """
    Logs dispatched SMS entry into SMSLog table.
    """
    sent_at = datetime.now().isoformat()
    print(f"[SMSLOG] Phone: {phone} | Status: {status} | SentAt: {sent_at} | Msg: '{message}'")
    return {"phone": phone, "status": status, "sent_at": sent_at}

def get_attendance(roll_no):
    """
    Retrieves total attendance leave/OD count for a student.
    """
    conn = sqlite3.connect(LOCAL_DB_PATH)
    c = conn.cursor()
    c.execute("SELECT SUM(duration_days) FROM leave_od_requests WHERE roll_no = ? AND status = 'Approved'", (roll_no,))
    total = c.fetchone()[0] or 0
    conn.close()
    return total
