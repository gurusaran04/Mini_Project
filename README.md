# AI-Driven Voice IVR Student Leave & On-Duty (OD) Management System

A cloud-based voice telephony and automated record management system designed for institutional student leave tracking, fraud-resistant caller ID verification, n8n workflow automation, real-time Class Advisor dashboards, and instant parent notifications via SMS/WhatsApp.

---

## 📁 Repository Structure (`D:\Mini_Project`)

```
D:\Mini_Project\
├── docker-compose.yml             # Docker stack for PostgreSQL, n8n, and Backend API
├── .env.example                   # Environment configuration template
├── server/
│   ├── package.json               # Node.js Express dependencies
│   ├── Dockerfile                 # Container file for backend service
│   └── server.js                  # Express REST API, Vapi webhook & DB persistence
├── tests/
│   └── test_ivr_flow.js           # Automated integration test suite
├── vapi/
│   ├── system_prompt.txt          # Polite Vapi.ai/Retell system prompt
│   └── vapi_assistant_config.json # Vapi voice engine config & tool payload schema
├── n8n/
│   ├── workflow_inbound_call.json # Workflow 1: Webhook -> Auth -> DB Write -> Email Alert
│   ├── workflow_advisor_action.json# Workflow 2: Advisor Action -> DB Update -> SMS/WhatsApp
│   └── nodes/
│       ├── parse_vapi_payload.js  # Node JS: Parse Vapi call payload & audio link
│       ├── validate_caller_id.js  # Node JS: Match Caller ID against Student Directory
│       └── format_whatsapp_template.js# Node JS: Format SMS/WhatsApp notification
├── database/
│   ├── schema.sql                 # PostgreSQL / Supabase schema & seed data
│   └── airtable_schema.json       # Airtable schema & field metadata
├── dashboard/
│   ├── index.html                 # Advisor & HOD Dashboard UI
│   ├── styles.css                 # Glassmorphism dark mode CSS
│   └── app.js                     # Real-time API state, filters & call simulator
└── README.md
```

---

## ⚡ Deployment Options

### Option A: One-Command Docker Deployment (Recommended)
1. Copy `.env.example` to `.env` and fill in your Vapi and Twilio keys.
2. Run:
   ```bash
   docker-compose up -d
   ```
3. Access services:
   - **Advisor Dashboard & API**: `http://localhost:3000`
   - **n8n Automation Engine**: `http://localhost:5678` (Login: `admin` / `admin123`)
   - **PostgreSQL Database**: `localhost:5432` (DB: `student_leave_db`)

### Option B: Standalone Web / Local Testing Mode
1. Open `dashboard/index.html` directly in any web browser.
2. Click **"📞 Simulate Parent Call"** to run call intake, verification, and advisor review offline.

---

## 🧪 Automated Testing

Run the test suite script to verify call payload parsing, caller ID verification, fraud rejection, and WhatsApp template formatting:
```bash
node tests/test_ivr_flow.js
```
