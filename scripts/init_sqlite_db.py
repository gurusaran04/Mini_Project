import sqlite3
import os

db_path = r"D:\Mini_Project\database\student_leave_db.sqlite"

# Create directory if missing
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Connect & Initialize SQLite Database File
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Faculty Advisors Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty_advisors (
    advisor_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    section TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Seed Faculty Advisor (Prof. Madhan)
cursor.execute("""
INSERT OR REPLACE INTO faculty_advisors (advisor_id, name, department, section, email, phone_number)
VALUES ('ADV-MADHAN-01', 'Prof. Madhan', 'Computer Science', '3-A', 'madhan@institution.edu', '+9118004258899');
""")

# 2. Students & Parent Directory Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students_parent_directory (
    roll_no TEXT PRIMARY KEY,
    student_name TEXT NOT NULL,
    department TEXT NOT NULL,
    year INTEGER CHECK (year BETWEEN 1 AND 4),
    section TEXT NOT NULL,
    parent_phone_number TEXT NOT NULL UNIQUE,
    parent_name TEXT NOT NULL,
    advisor_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (advisor_id) REFERENCES faculty_advisors(advisor_id)
);
""")

# Seed Sample Students & Authorized Parent Numbers
cursor.execute("""
INSERT OR IGNORE INTO students_parent_directory (roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id)
VALUES 
('21CS042', 'Alexander Wright', 'Computer Science', 3, '3-A', '+15559876543', 'Robert Wright', 'ADV-MADHAN-01'),
('22EC015', 'Maya Lin', 'Electronics', 2, '2-B', '+15558765432', 'David Lin', 'ADV-MADHAN-01');
""")

# 3. Leave & OD Requests Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS leave_od_requests (
    request_id TEXT PRIMARY KEY,
    roll_no TEXT NOT NULL,
    request_type TEXT NOT NULL CHECK (request_type IN ('Leave', 'OD')),
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    reason TEXT NOT NULL,
    ivr_call_sid TEXT,
    recording_url TEXT,
    status TEXT NOT NULL DEFAULT 'Pending',
    advisor_notes TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (roll_no) REFERENCES students_parent_directory(roll_no)
);
""")

# Seed Sample Leave and OD Requests
cursor.execute("""
INSERT OR IGNORE INTO leave_od_requests (request_id, roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status, advisor_notes)
VALUES 
('REQ-9012', '21CS042', 'Leave', '2026-08-06', '2026-08-08', 3, 'High fever and viral infection. Doctor advised 3 days bed rest.', 'CA-9817264812', 'https://api.vapi.ai/recordings/sample-1.mp3', 'Pending', ''),
('REQ-8871', '22EC015', 'OD', '2026-08-07', '2026-08-07', 1, 'Representing college at State Level Robotics Hackathon at IIT.', 'CA-4481920192', 'https://api.vapi.ai/recordings/sample-2.mp3', 'Approved', 'Approved. All the best for the hackathon!');
""")

conn.commit()
conn.close()

print(f"SUCCESS: SQLite Database created and seeded at {db_path}")
