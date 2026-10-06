import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
from datetime import datetime

PORT = 3000
DB_PATH = r"D:\Mini_Project\database\student_leave_db.sqlite"
DASHBOARD_DIR = r"D:\Mini_Project\dashboard"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS faculty_advisors (
        advisor_id TEXT PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL,
        section TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone_number TEXT NOT NULL
    );
    """)
    c.execute("""
    INSERT OR REPLACE INTO faculty_advisors (advisor_id, name, department, section, email, phone_number)
    VALUES ('ADV-MADHAN-01', 'Prof. Madhan', 'Computer Science', '3-A', 'madhan@institution.edu', '+9118004258899');
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS students_parent_directory (
        roll_no TEXT PRIMARY KEY, student_name TEXT NOT NULL, department TEXT NOT NULL,
        year INTEGER CHECK (year BETWEEN 1 AND 4), section TEXT NOT NULL,
        parent_phone_number TEXT NOT NULL UNIQUE, parent_name TEXT NOT NULL, advisor_id TEXT
    );
    """)
    c.execute("""
    INSERT OR IGNORE INTO students_parent_directory (roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id)
    VALUES 
    ('21CS042', 'Alexander Wright', 'Computer Science', 3, '3-A', '+15559876543', 'Robert Wright', 'ADV-MADHAN-01'),
    ('22EC015', 'Maya Lin', 'Electronics', 2, '2-B', '+15558765432', 'David Lin', 'ADV-MADHAN-01');
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS leave_od_requests (
        request_id TEXT PRIMARY KEY, roll_no TEXT NOT NULL, request_type TEXT NOT NULL,
        start_date TEXT NOT NULL, end_date TEXT NOT NULL, duration_days INTEGER NOT NULL,
        reason TEXT NOT NULL, ivr_call_sid TEXT, recording_url TEXT, status TEXT NOT NULL DEFAULT 'Pending',
        advisor_notes TEXT, reviewed_at TIMESTAMP, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    c.execute("""
    INSERT OR IGNORE INTO leave_od_requests (request_id, roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status, advisor_notes)
    VALUES 
    ('REQ-9012', '21CS042', 'Leave', '2026-08-06', '2026-08-08', 3, 'High fever and viral infection. Doctor advised 3 days bed rest.', 'CA-9817264812', 'https://api.vapi.ai/recordings/sample-1.mp3', 'Pending', ''),
    ('REQ-8871', '22EC015', 'OD', '2026-08-07', '2026-08-07', 1, 'Representing college at State Level Robotics Hackathon at IIT.', 'CA-4481920192', 'https://api.vapi.ai/recordings/sample-2.mp3', 'Approved', 'Approved. All the best for the hackathon!');
    """)
    conn.commit()
    conn.close()

init_db()

class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        clean_path = path.split('?')[0]
        if clean_path.startswith('/api/'):
            return super().translate_path(path)
        req_path = os.path.normpath(urllib.parse.unquote(clean_path))
        if req_path in ['/', '\\', '']:
            req_path = '/index.html'
        full_path = os.path.join(DASHBOARD_DIR, req_path.lstrip('/\\'))
        return full_path

    def do_GET(self):
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
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
            SELECT r.request_id, r.roll_no, r.request_type, r.start_date, r.end_date, r.duration_days, r.reason, r.ivr_call_sid, r.recording_url, r.status, r.advisor_notes, r.created_at, s.student_name, s.department, s.section, s.parent_name, s.parent_phone_number
            FROM leave_od_requests r
            JOIN students_parent_directory s ON r.roll_no = s.roll_no
            ORDER BY r.created_at DESC
            """)
            rows = c.fetchall()
            conn.close()
            data = [{
                "request_id": r[0], "roll_no": r[1], "request_type": r[2], "start_date": r[3], "end_date": r[4],
                "duration_days": r[5], "reason": r[6], "ivr_call_sid": r[7], "recording_url": r[8], "status": r[9],
                "advisor_notes": r[10], "created_at": r[11], "student_name": r[12], "department": r[13],
                "section": r[14], "parent_name": r[15], "parent_phone_number": r[16]
            } for r in rows]
            self.wfile.write(json.dumps({"success": True, "data": data}).encode())
            return

        super().do_GET()

    def do_DELETE(self):
        if self.path.startswith('/api/directory/'):
            roll_no = urllib.parse.unquote(self.path.split('/')[-1])
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM leave_od_requests WHERE roll_no = ?", (roll_no,))
            c.execute("DELETE FROM students_parent_directory WHERE roll_no = ?", (roll_no,))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": f"Deleted student record {roll_no}"}).encode())
            return
        
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8')
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

        elif self.path.startswith('/api/webhook/vapi-end-call'):
            caller_phone = ""
            if 'message' in body and 'customer' in body['message']:
                caller_phone = body['message']['customer'].get('number', '')
            elif 'caller_id' in body:
                caller_phone = body['caller_id']

            call_sid = "CALL-" + str(int(datetime.now().timestamp()))
            if 'message' in body and 'call' in body['message']:
                call_sid = body['message']['call'].get('id', call_sid)

            recording_url = ""
            if 'message' in body:
                recording_url = body['message'].get('recordingUrl', '')

            func_args = {}
            if 'message' in body and 'toolCalls' in body['message'] and len(body['message']['toolCalls']) > 0:
                func_args = body['message']['toolCalls'][0]['function'].get('arguments', {})

            req_type = func_args.get('requestType', 'Leave')
            start_date = func_args.get('startDate', datetime.now().strftime('%Y-%m-%d'))
            end_date = func_args.get('endDate', start_date)
            duration_days = int(func_args.get('durationDays', 1))
            reason = func_args.get('reason', 'Voice IVR Submission')

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT roll_no, student_name FROM students_parent_directory WHERE parent_phone_number = ?", (caller_phone,))
            row = c.fetchone()

            if not row:
                conn.close()
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "UNAUTHORIZED_CALLER_ID", "message": f"Caller ID {caller_phone} not registered."}).encode())
                return

            req_id = "REQ-" + str(int(datetime.now().timestamp()))
            c.execute("""
            INSERT INTO leave_od_requests (request_id, roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
            """, (req_id, row[0], req_type, start_date, end_date, duration_days, reason, call_sid, recording_url))
            conn.commit()
            conn.close()

            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": "Request logged", "requestId": req_id}).encode())
            return

        elif '/action' in self.path:
            parts = self.path.split('/')
            req_id = parts[3] if len(parts) > 3 else ""
            status = body.get('status', 'Approved')
            notes = body.get('advisorNotes', '')

            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("UPDATE leave_od_requests SET status = ?, advisor_notes = ?, reviewed_at = CURRENT_TIMESTAMP WHERE request_id = ?", (status, notes, req_id))
            conn.commit()
            conn.close()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "message": f"Request {req_id} updated to {status}"}).encode())
            return

        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print(f"[SERVER STARTED] Production Python Server running on http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), UnifiedHandler) as httpd:
    httpd.serve_forever()
