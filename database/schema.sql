/* 
  AI-Driven Voice IVR Student Leave and On-Duty (OD) Management System
  Production Database Schema for PostgreSQL / Supabase
*/

-- 1. Faculty Advisors Table
CREATE TABLE IF NOT EXISTS faculty_advisors (
    advisor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    section VARCHAR(10) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed Faculty Advisor Profile (Prof. Madhan)
INSERT INTO faculty_advisors (advisor_id, name, department, section, email, phone_number) VALUES
('ADV-MADHAN-01', 'Prof. Madhan', 'Computer Science', '3-A', 'madhan@institution.edu', '+9118004258899')
ON CONFLICT (advisor_id) DO NOTHING;

-- 2. Students & Parent Directory Table (Managed by Class Advisor Prof. Madhan)
CREATE TABLE IF NOT EXISTS students_parent_directory (
    roll_no VARCHAR(50) PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    year INT CHECK (year BETWEEN 1 AND 4),
    section VARCHAR(10) NOT NULL,
    parent_phone_number VARCHAR(20) NOT NULL UNIQUE,
    parent_name VARCHAR(100) NOT NULL,
    advisor_id VARCHAR(50) REFERENCES faculty_advisors(advisor_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index on parent phone number for instant caller ID lookup during IVR calls
CREATE INDEX IF NOT EXISTS idx_parent_phone ON students_parent_directory(parent_phone_number);

-- 3. Leave & OD Requests Table (Populated dynamically when parents call the IVR number)
CREATE TABLE IF NOT EXISTS leave_od_requests (
    request_id VARCHAR(50) PRIMARY KEY DEFAULT ('REQ-' || gen_random_uuid()),
    roll_no VARCHAR(50) NOT NULL REFERENCES students_parent_directory(roll_no) ON DELETE CASCADE,
    request_type VARCHAR(10) NOT NULL CHECK (request_type IN ('Leave', 'OD')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    duration_days INT NOT NULL,
    reason TEXT NOT NULL,
    ivr_call_sid VARCHAR(100),
    recording_url TEXT,
    call_duration_seconds INT,
    status VARCHAR(20) NOT NULL DEFAULT 'TRANSCRIPT_UPLOADED',
    advisor_notes TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for status filtering
CREATE INDEX IF NOT EXISTS idx_request_status ON leave_od_requests(status);
CREATE INDEX IF NOT EXISTS idx_roll_no ON leave_od_requests(roll_no);
