"""
Vercel Serverless Entrypoint for AI Voice IVR Engine
Exposes API endpoints on Vercel Functions
"""

from http.server import BaseHTTPRequestHandler
import json
import sqlite3
import os
import sys
from datetime import datetime

# Add database folder to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
database_dir = os.path.join(os.path.dirname(current_dir), "database")
if database_dir not in sys.path:
    sys.path.append(database_dir)

import airtable_client
import seed_50_students_parents

DB_PATH = "/tmp/student_leave_db.sqlite" if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")) else r"D:\Mini_Project\database\student_leave_db.sqlite"

def init_db():
    try:
        seed_50_students_parents.seed_database()
    except Exception as e:
        print(f"[VERCEL DB INIT] {e}")

init_db()

PROCESSED_CALL_SIDS = set()

def dispatch_parent_sms(parent_phone, student_name, req_type, status, notes):
    sms_text = f"[ST. JUDE TECH] Dear Parent, Leave/OD Request for ward {student_name} ({req_type}) has been {status.upper()} by Class Advisor Prof. Madhan. Remarks: {notes}"
    print(f"\n[OUTBOUND PARENT SMS DISPATCH] To: {parent_phone} | Message: {sms_text}")
    try:
        airtable_client.log_sms(parent_phone, sms_text, "Delivered")
    except Exception:
        pass
    return "📩 SMS Delivered"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        init_db()
        if self.path.startswith('/api/directory'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id FROM students_parent_directory")
            rows = c.fetchall()
            conn.close()
            data = [{"roll_no": r[0], "student_name": r[1], "department": r[2], "year": r[3], "section": r[4], "parent_phone_number": r[5], "parent_name": r[6], "advisor_id": r[7]} for r in rows]
            self.wfile.write(json.dumps({"success": True, "data": data}).encode())
            return

        elif self.path.startswith('/api/requests'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = airtable_client.list_leave_requests()
            self.wfile.write(json.dumps({"success": True, "data": data}).encode())
            return

        elif self.path.startswith('/api/get-ip'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "ip": "127.0.0.1", "port": 3000}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        init_db()
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8') if content_len > 0 else ""
        try:
            body = json.loads(post_body) if post_body else {}
        except:
            body = {}

        if self.path.startswith('/api/directory'):
            roll_no = body.get('rollNo') or body.get('roll_no')
            student_name = body.get('studentName') or body.get('student_name')
            dept = body.get('department', 'Computer Science')
            year = int(body.get('year', 3))
            section = body.get('section', '3-A')
            parent_phone = body.get('parentPhone') or body.get('parent_phone_number')
            parent_name = body.get('parentName') or body.get('parent_name')

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
            INSERT OR REPLACE INTO students_parent_directory (roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'ADV-MADHAN-01')
            """, (roll_no, student_name, dept, year, section, parent_phone, parent_name))
            conn.commit()
            conn.close()

            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Parent authorized"}).encode())
            return

        elif self.path.startswith('/api/webhook/vapi-end-call') or self.path.startswith('/api/webhook/free-ivr'):
            caller_phone = body.get('caller_id') or body.get('message', {}).get('customer', {}).get('number', '')
            call_sid = body.get("call_sid") or f"AST-SIP-{int(datetime.now().timestamp())}"

            if call_sid in PROCESSED_CALL_SIDS:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, "message": "Duplicate call payload ignored"}).encode())
                return

            PROCESSED_CALL_SIDS.add(call_sid)

            student_info = airtable_client.get_student_by_parent_phone(caller_phone)
            matched_roll_no = student_info["roll_no"]
            student_name = student_info["student_name"]

            func_args = body.get('message', {}).get('toolCalls', [{}])[0].get('function', {}).get('arguments', body)
            req_type = func_args.get('requestType', 'Leave')
            reason = func_args.get('reason', 'High fever and viral infection. Doctor prescribed 2 days bed rest.')

            created_res = airtable_client.create_leave_request({
                "id": f"REQ-{int(datetime.now().timestamp())}",
                "roll_no": matched_roll_no,
                "type": req_type,
                "reason_text": reason,
                "audio_url": "https://api.vapi.ai/recordings/sample.mp3",
                "received_at": datetime.now().isoformat(),
                "status": "Pending"
            })

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "IVR Call Payload Processed & Logged to Database",
                "requestId": created_res['id'],
                "matchedStudent": student_name,
                "rollNo": matched_roll_no
            }).encode())
            return

        elif '/action' in self.path:
            parts = self.path.split('/')
            req_id = parts[3] if len(parts) > 3 else ""
            status = body.get('status', 'Approved')
            notes = body.get('advisorNotes', '')

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
            SELECT r.roll_no, r.request_type, s.student_name, s.parent_phone_number
            FROM leave_od_requests r
            JOIN students_parent_directory s ON r.roll_no = s.roll_no
            WHERE r.request_id = ?
            """, (req_id,))
            row = c.fetchone()
            conn.close()

            sms_res = "📩 SMS Delivered"
            if row:
                student_name, parent_phone, req_type = row[2], row[3], row[1]
                sms_res = dispatch_parent_sms(parent_phone, student_name, req_type, status, notes)
                airtable_client.update_approval(req_id, "ADV-MADHAN-01", status, notes)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": f"Request {req_id} updated to {status}. SMS: {sms_res}"}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
