"""
DATABASE SEEDER SCRIPT: seed_50_students_parents.py
Populates SQLite database (student_leave_db.sqlite) with 50 realistic linked student-parent records
and 25 Leave/OD requests across Pending, Approved, and Rejected statuses.
"""

import sqlite3
import os
import random
from datetime import datetime, timedelta

DB_PATH = "/tmp/student_leave_db.sqlite" if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")) else r"D:\Mini_Project\database\student_leave_db.sqlite"

STUDENT_FIRST_NAMES = [
    "GuruSaran", "Alexander", "Maya", "Aarav", "Ananya", "Rohan", "Priya", "Karthik", "Sneha", "Vikram",
    "Divya", "Sanjay", "Kavya", "Rahul", "Meera", "Arjun", "Pooja", "Varun", "Deepika", "Aditya",
    "Ritu", "Nitin", "Nisha", "Gautam", "Shruti", "Manish", "Swati", "Rajesh", "Neha", "Abhishek",
    "Preeti", "Suresh", "Anita", "Dinesh", "Rashmi", "Alok", "Sunita", "Harish", "Aarti", "Pawan",
    "Kiran", "Tarun", "Bhavna", "Vishal", "Monika", "Sachin", "Payal", "Rakesh", "Shweta", "Amit"
]

STUDENT_LAST_NAMES = [
    "Periyasamy", "Wright", "Lin", "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Singh",
    "Kumar", "Gupta", "Joshi", "Rao", "Deshmukh", "Chaudhary", "Malhotra", "Mehta", "Bhat", "Saxena",
    "Agarwal", "Bansal", "Kapoor", "Thakur", "Mishra", "Pandey", "Trivedi", "Shukla", "Dube", "Sinha"
]

DEPARTMENTS = ["Computer Science", "Electronics", "Mechanical", "Civil"]
SECTIONS = ["3-A", "3-B", "2-A", "2-B", "4-A"]
REASON_TEMPLATES_LEAVE = [
    "High fever and severe cold. Doctor prescribed 2 days bed rest.",
    "Viral flu and throat infection. Advised home isolation for 3 days.",
    "Severe migraine and eye strain. Doctor recommended rest.",
    "Acute stomach pain and food poisoning. Prescribed medications.",
    "Attending elder sister's wedding ceremony in native town.",
    "Family emergency and urgent domestic work.",
    "Sprained ankle during sports practice. Doctor advised rest."
]

REASON_TEMPLATES_OD = [
    "Representing college at State Level Robotics Hackathon at IIT Madras.",
    "Attending National Level Technical Symposium & Paper Presentation.",
    "Participating in Inter-College Athletic Meet & Football Tournament.",
    "Attending Industrial Visit & Smart City Workshop at Tech Park.",
    "Presenting AI Research Paper at IEEE Student Conference."
]

def seed_database():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Re-create tables
        c.execute("""
        CREATE TABLE IF NOT EXISTS faculty_advisors (
            advisor_id TEXT PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL,
            section TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone_number TEXT NOT NULL
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS students_parent_directory (
            roll_no TEXT PRIMARY KEY, student_name TEXT NOT NULL, department TEXT NOT NULL,
            year INTEGER CHECK (year BETWEEN 1 AND 4), section TEXT NOT NULL,
            parent_phone_number TEXT NOT NULL UNIQUE, parent_name TEXT NOT NULL, advisor_id TEXT
        );
        """)

        c.execute("""
        CREATE TABLE IF NOT EXISTS leave_od_requests (
            request_id TEXT PRIMARY KEY, roll_no TEXT NOT NULL, request_type TEXT NOT NULL,
            start_date TEXT NOT NULL, end_date TEXT NOT NULL, duration_days INTEGER NOT NULL,
            reason TEXT NOT NULL, ivr_call_sid TEXT, recording_url TEXT, status TEXT NOT NULL DEFAULT 'Pending',
            advisor_notes TEXT, sms_status TEXT DEFAULT 'Pending Review', reviewed_at TIMESTAMP, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # 1. Insert Faculty Advisor
        c.execute("""
        INSERT OR REPLACE INTO faculty_advisors (advisor_id, name, department, section, email, phone_number)
        VALUES ('ADV-MADHAN-01', 'Prof. Madhan', 'Computer Science', '3-A', 'madhan@institution.edu', '+9118004258899');
        """)

        # Clear old records for clean 50-student seeding
        c.execute("DELETE FROM leave_od_requests;")
        c.execute("DELETE FROM students_parent_directory;")

        # 2. Seed 50 Linked Student-Parent Records
        student_records = []
        for i in range(1, 51):
            roll_no = f"21CS{i:03d}"
            fname = STUDENT_FIRST_NAMES[i-1]
            lname = STUDENT_LAST_NAMES[i % len(STUDENT_LAST_NAMES)]
            sname = f"{fname} {lname}"
            dept = DEPARTMENTS[(i-1) % len(DEPARTMENTS)]
            year = random.choice([2, 3, 4])
            sec = SECTIONS[(i-1) % len(SECTIONS)]
            
            # Parent details
            p_fname = random.choice(["Robert", "David", "Periyasamy", "Ramesh", "Suresh", "Venkatesh", "Sundar", "Vijay", "Anand", "Baskar"])
            parent_name = f"{p_fname} {lname}"
            
            if i == 47:
                parent_phone = "+919087598993"
                sname = "GuruSaran"
                parent_name = "Periyasamy"
                roll_no = "21CS047"
            elif i == 42:
                parent_phone = "+15559876543"
                sname = "Alexander Wright"
                parent_name = "Robert Wright"
                roll_no = "21CS042"
            elif i == 15:
                parent_phone = "+15558765432"
                sname = "Maya Lin"
                parent_name = "David Lin"
                roll_no = "22EC015"
            else:
                parent_phone = f"+9190875{i:05d}"

            student_records.append((roll_no, sname, dept, year, sec, parent_phone, parent_name, "ADV-MADHAN-01"))

        c.executemany("""
        INSERT OR REPLACE INTO students_parent_directory (roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, student_records)

        # 3. Seed 25 Leave & OD Requests
        request_records = []
        statuses = ["Pending", "Approved", "Approved", "Rejected"]
        
        for req_idx in range(1, 26):
            student = student_records[(req_idx - 1) * 2]
            roll_no = student[0]
            req_type = "OD" if (req_idx % 3 == 0) else "Leave"
            
            days = random.choice([1, 2, 3])
            start_dt = datetime.now() - timedelta(days=random.randint(1, 15))
            end_dt = start_dt + timedelta(days=days-1)
            
            start_str = start_dt.strftime('%Y-%m-%d')
            end_str = end_dt.strftime('%Y-%m-%d')
            
            reason = random.choice(REASON_TEMPLATES_OD) if req_type == "OD" else random.choice(REASON_TEMPLATES_LEAVE)
            status = statuses[(req_idx - 1) % len(statuses)]
            
            req_id = f"REQ-{9000 + req_idx}"
            call_sid = f"AST-SIP-{int(start_dt.timestamp()) + req_idx}"
            recording_url = f"https://api.vapi.ai/recordings/sample-{req_idx}.mp3"
            
            notes = "Approved by Class Advisor Prof. Madhan." if status == "Approved" else ("Rejected due to upcoming mid-term exams." if status == "Rejected" else "")
            sms_status = "📩 SMS Delivered" if status != "Pending" else "⏳ Pending Review"
            reviewed_at = (datetime.now() - timedelta(hours=req_idx)).strftime('%Y-%m-%d %H:%M:%S') if status != "Pending" else None

            request_records.append((
                req_id, roll_no, req_type, start_str, end_str, days, reason,
                call_sid, recording_url, status, notes, sms_status, reviewed_at
            ))

        c.executemany("""
        INSERT OR REPLACE INTO leave_od_requests (request_id, roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status, advisor_notes, sms_status, reviewed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, request_records)

        conn.commit()
        conn.close()

        print(f"[SEEDER SUCCESS] Successfully seeded 50 Linked Student-Parent records and 25 Leave/OD requests into {DB_PATH}!")
    except Exception as e:
        print(f"[SEEDER NOTICE] Database initialization info: {e}")

if __name__ == "__main__":
    seed_database()
