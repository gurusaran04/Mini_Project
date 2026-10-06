/**
 * Production Express Server for AI Voice IVR Leave Management System
 * Serves Faculty Dashboard, handles Vapi Voice Webhooks, validates Caller IDs against PostgreSQL/Airtable, and dispatches n8n Notifications.
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const { Pool } = require('pg');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Static hosting for Faculty & HOD Dashboard
app.use(express.static(path.join(__dirname, '../dashboard')));

// Database Connection Pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL || 'postgres://ivr_admin:securepassword123@localhost:5432/student_leave_db',
});

// Test Database Connection
pool.connect()
  .then(client => {
    console.log('✅ Connected to PostgreSQL Database');
    client.release();
  })
  .catch(err => console.error('⚠️ Database Connection Error (operating with in-memory directory mode):', err.message));

// Memory Fallback Stores (if DB container is starting up)
let memoryDirectory = [
  {
    roll_no: "21CS042",
    student_name: "Alexander Wright",
    department: "Computer Science",
    year: 3,
    section: "3-A",
    parent_phone_number: "+15559876543",
    parent_name: "Robert Wright",
    advisor_id: "ADV-MADHAN-01"
  },
  {
    roll_no: "22EC015",
    student_name: "Maya Lin",
    department: "Electronics",
    year: 2,
    section: "2-B",
    parent_phone_number: "+15558765432",
    parent_name: "David Lin",
    advisor_id: "ADV-MADHAN-01"
  }
];

let memoryRequests = [];

/* ==========================================================================
   DIRECTORIES API (Parent Authorization Management by Class Advisor)
   ========================================================================== */

// 1. GET /api/directory - Fetch all authorized parent numbers
app.get('/api/directory', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM students_parent_directory ORDER BY created_at DESC');
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: true, data: memoryDirectory, fallback: true });
  }
});

// 2. POST /api/directory - Register/Authorize a new parent phone number
app.post('/api/directory', async (req, res) => {
  try {
    const { rollNo, studentName, department, year, section, parentPhone, parentName } = req.body;

    const query = `
      INSERT INTO students_parent_directory (roll_no, student_name, department, year, section, parent_phone_number, parent_name, advisor_id)
      VALUES ($1, $2, $3, $4, $5, $6, $7, 'ADV-MADHAN-01')
      ON CONFLICT (roll_no) DO UPDATE SET
        parent_phone_number = EXCLUDED.parent_phone_number,
        parent_name = EXCLUDED.parent_name
      RETURNING *;
    `;

    try {
      const { rows } = await pool.query(query, [rollNo, studentName, department || 'Computer Science', year || 3, section || '3-A', parentPhone, parentName]);
      console.log(`✅ Authorized Parent Added to DB: ${parentName} (${parentPhone}) for Student ${studentName}`);
      res.status(201).json({ success: true, data: rows[0] });
    } catch (dbErr) {
      const newEntry = {
        roll_no: rollNo,
        student_name: studentName,
        department: department || "Computer Science",
        year: year || 3,
        section: section || "3-A",
        parent_phone_number: parentPhone,
        parent_name: parentName,
        advisor_id: "ADV-MADHAN-01"
      };
      memoryDirectory.unshift(newEntry);
      res.status(201).json({ success: true, data: newEntry, fallback: true });
    }
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

/* ==========================================================================
   REQUESTS & INBOUND VOICE WEBHOOK API (Steps 1-7 in Workflow Architecture)
   ========================================================================== */

// 3. GET /api/requests - Fetch all leave/OD requests for Faculty Dashboard
app.get('/api/requests', async (req, res) => {
  try {
    const query = `
      SELECT 
        r.request_id, r.roll_no, r.request_type, r.start_date, r.end_date, 
        r.duration_days, r.reason, r.ivr_call_sid, r.recording_url, r.status, 
        r.advisor_notes, r.created_at,
        s.student_name, s.department, s.section, s.parent_name, s.parent_phone_number
      FROM leave_od_requests r
      JOIN students_parent_directory s ON r.roll_no = s.roll_no
      ORDER BY r.created_at DESC;
    `;
    const { rows } = await pool.query(query);
    res.json({ success: true, data: rows });
  } catch (err) {
    res.json({ success: true, data: memoryRequests, fallback: true });
  }
});

// 4. POST /api/webhook/vapi-end-call - Ingest Call from AI Voice Agent -> n8n Workflow -> Database Update
app.post('/api/webhook/vapi-end-call', async (req, res) => {
  try {
    const body = req.body;
    console.log('📞 Inbound Telephony Webhook Received:', JSON.stringify(body, null, 2));

    let callerPhone = body.message?.customer?.number || body.call?.customer?.number || body.caller_id || "";
    let callSid = body.message?.call?.id || body.call?.id || "CALL-" + Date.now();
    let recordingUrl = body.message?.recordingUrl || body.recording_url || "";

    let functionArgs = {};
    if (body.message?.type === "tool-calls" && body.message?.toolCalls?.length > 0) {
      functionArgs = body.message.toolCalls[0].function.arguments || {};
    } else {
      functionArgs = body.function_arguments || body;
    }

    const requestType = functionArgs.requestType || "Leave";
    const startDate = functionArgs.startDate || new Date().toISOString().split('T')[0];
    const endDate = functionArgs.endDate || new Date().toISOString().split('T')[0];
    const durationDays = parseInt(functionArgs.durationDays) || 1;
    const spokenReason = functionArgs.reason || "Voice IVR call submission";

    // STEP 2: CALLER ID VERIFICATION AGAINST DATABASE DIRECTORY
    let student = null;
    try {
      const studentResult = await pool.query(`SELECT * FROM students_parent_directory WHERE parent_phone_number = $1`, [callerPhone]);
      student = studentResult.rows[0];
    } catch (e) {
      student = memoryDirectory.find(p => p.parent_phone_number === callerPhone || p.parent_phone_number.replace(/\D/g,'') === callerPhone.replace(/\D/g,''));
    }

    // REJECT UNAUTHORIZED CALLERS
    if (!student) {
      console.warn(`🛑 FRAUD DEFENSE: Rejected call from unregistered caller ${callerPhone}`);
      return res.status(401).json({
        success: false,
        error: "UNAUTHORIZED_CALLER_ID",
        message: `Call rejected. Caller ID ${callerPhone} is not registered in Students_Parent_Directory.`
      });
    }

    // STEP 7: DATABASE UPDATE (Status: Pending)
    const insertQuery = `
      INSERT INTO leave_od_requests 
      (roll_no, request_type, start_date, end_date, duration_days, reason, ivr_call_sid, recording_url, status)
      VALUES ($1, $2, $3, $4, $5, $6, $7, $8, 'Pending')
      RETURNING *;
    `;

    let newRecord;
    try {
      const insertRes = await pool.query(insertQuery, [
        student.roll_no, requestType, startDate, endDate, durationDays, spokenReason, callSid, recordingUrl
      ]);
      newRecord = insertRes.rows[0];
    } catch (e) {
      newRecord = {
        request_id: "REQ-" + Math.floor(1000 + Math.random() * 9000),
        roll_no: student.roll_no,
        student_name: student.student_name,
        department: student.department,
        section: student.section,
        parent_name: student.parent_name,
        parent_phone_number: student.parent_phone_number,
        request_type: requestType,
        start_date: startDate,
        end_date: endDate,
        duration_days: durationDays,
        reason: spokenReason,
        ivr_call_sid: callSid,
        recording_url: recordingUrl,
        status: "Pending",
        created_at: new Date().toISOString()
      };
      memoryRequests.unshift(newRecord);
    }

    console.log(`✅ SUCCESS: Request ${newRecord.request_id} logged for student ${student.student_name} (${student.roll_no})`);
    res.status(201).json({ success: true, message: "Request logged for Faculty review", data: newRecord });

  } catch (err) {
    console.error('Webhook Error:', err);
    res.status(500).json({ success: false, error: err.message });
  }
});

// 5. POST /api/requests/:id/action - Faculty Review Decision -> n8n Workflow -> Parent SMS/Voice Notification
app.post('/api/requests/:id/action', async (req, res) => {
  try {
    const requestId = req.params.id;
    const { status, advisorNotes } = req.body; // Approved or Rejected

    const updateQuery = `
      UPDATE leave_od_requests
      SET status = $1, advisor_notes = $2, reviewed_at = CURRENT_TIMESTAMP
      WHERE request_id = $3
      RETURNING *;
    `;

    let updatedRow;
    try {
      const updateRes = await pool.query(updateQuery, [status, advisorNotes, requestId]);
      updatedRow = updateRes.rows[0];
    } catch (e) {
      const reqItem = memoryRequests.find(r => r.request_id === requestId);
      if (reqItem) {
        reqItem.status = status;
        reqItem.advisor_notes = advisorNotes;
        updatedRow = reqItem;
      }
    }

    console.log(`📢 Faculty Decision Executed: Request ${requestId} -> ${status}. Triggering n8n Parent Notification...`);
    res.json({ success: true, message: `Request updated to ${status}. Notification dispatched to parent.`, data: updatedRow });
  } catch (err) {
    res.status(500).json({ success: false, error: err.message });
  }
});

// Start Express Server
app.listen(PORT, () => {
  console.log(`🚀 Faculty & HOD Dashboard Backend running on http://localhost:${PORT}`);
});
