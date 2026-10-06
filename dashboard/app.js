/**
 * Faculty & HOD Dashboard - Complete Production Application Logic
 * Supports Individual & Bulk CSV Parent Number Import, PSTN Direct Mobile SIM Calling, and IVR Workflow.
 * Hardcoded with 50 Seeded Student-Parent Records for Instant Offline & Online Compatibility.
 */

const API_BASE_URL = (typeof window !== "undefined" && window.location && window.location.hostname && (window.location.hostname.includes("aura-ivr") || window.location.origin.includes("3000") || window.location.origin.includes("8080")))
  ? `${window.location.protocol}//${window.location.hostname}:3000`
  : "http://localhost:3000";

const FIRST_NAMES = [
  "GuruSaran", "Alexander", "Maya", "Aarav", "Ananya", "Rohan", "Priya", "Karthik", "Sneha", "Vikram",
  "Divya", "Sanjay", "Kavya", "Rahul", "Meera", "Arjun", "Pooja", "Varun", "Deepika", "Aditya",
  "Ritu", "Nitin", "Nisha", "Gautam", "Shruti", "Manish", "Swati", "Rajesh", "Neha", "Abhishek",
  "Preeti", "Suresh", "Anita", "Dinesh", "Rashmi", "Alok", "Sunita", "Harish", "Aarti", "Pawan",
  "Kiran", "Tarun", "Bhavna", "Vishal", "Monika", "Sachin", "Payal", "Rakesh", "Shweta", "Amit"
];

const LAST_NAMES = [
  "Periyasamy", "Wright", "Lin", "Sharma", "Verma", "Patel", "Reddy", "Nair", "Iyer", "Singh",
  "Kumar", "Gupta", "Joshi", "Rao", "Deshmukh", "Chaudhary", "Malhotra", "Mehta", "Bhat", "Saxena"
];

const DEPTS = ["Computer Science", "Electronics", "Mechanical", "Civil"];
const SECS = ["3-A", "3-B", "2-A", "2-B", "4-A"];
const PARENT_PREFIXES = ["Robert", "David", "Periyasamy", "Ramesh", "Suresh", "Venkatesh", "Sundar", "Vijay", "Anand", "Baskar"];

// Generate 50 Seeded Student-Parent Records
let parentDirectory = Array.from({ length: 50 }, (_, i) => {
  const idx = i + 1;
  const rollNo = idx === 1 ? "21CS047" : (idx === 2 ? "21CS042" : (idx === 3 ? "22EC015" : `21CS${String(idx).padStart(3, '0')}`));
  const sname = idx === 1 ? "GuruSaran" : (idx === 2 ? "Alexander Wright" : (idx === 3 ? "Maya Lin" : `${FIRST_NAMES[i]} ${LAST_NAMES[i % LAST_NAMES.length]}`));
  const phone = idx === 1 ? "+919087598993" : (idx === 2 ? "+15559876543" : (idx === 3 ? "+15558765432" : `+9190875${String(idx).padStart(5, '0')}`));
  const pname = idx === 1 ? "Periyasamy" : (idx === 2 ? "Robert Wright" : (idx === 3 ? "David Lin" : `${PARENT_PREFIXES[i % PARENT_PREFIXES.length]} ${LAST_NAMES[i % LAST_NAMES.length]}`));
  
  return {
    rollNo,
    studentName: sname,
    department: DEPTS[i % DEPTS.length],
    year: (i % 3) + 2,
    section: SECS[i % SECS.length],
    parentName: pname,
    parentPhone: phone,
    advisorId: "ADV-MADHAN-01"
  };
});

// Generate 25 Historical Leave & OD Requests
let leaveRequests = Array.from({ length: 25 }, (_, i) => {
  const idx = i + 1;
  const student = parentDirectory[(i * 2) % 50];
  const isOD = idx % 3 === 0;
  const status = (idx % 4 === 0) ? "Rejected" : ((idx % 2 === 0) ? "Approved" : "Pending");
  
  return {
    requestId: `REQ-${9000 + idx}`,
    rollNo: student.rollNo,
    studentName: student.studentName,
    department: student.department,
    section: student.section,
    parentName: student.parentName,
    parentPhone: student.parentPhone,
    type: isOD ? "OD" : "Leave",
    startDate: "2026-09-20",
    endDate: "2026-09-21",
    durationDays: isOD ? 1 : 2,
    reason: isOD ? "Representing college at State Level Robotics Hackathon at IIT." : "High fever and doctor prescribed 2 days bed rest.",
    ivrCallSid: `CA-98172${idx}00`,
    recordingUrl: `https://api.vapi.ai/recordings/sample-${idx}.mp3`,
    status: status,
    advisorNotes: status === "Approved" ? "Approved by Class Advisor Prof. Madhan." : (status === "Rejected" ? "Rejected due to upcoming mid-term exams." : ""),
    timestamp: `2026-09-20 10:${String(idx).padStart(2, '0')} AM`
  };
});

let activeTab = "all";
let activeFilterType = "ALL";
let searchQuery = "";
let selectedRequestId = null;
let selectedDtmfKey = "1";
let recognition = null;

document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

function initApp() {
  fetchDirectoryFromAPI();
  fetchRequestsFromAPI();
  setupEventListeners();
  setupSpeechRecognition();
  render();

  setInterval(() => {
    fetchDirectoryFromAPI();
    fetchRequestsFromAPI();
  }, 3000);
}

async function fetchDirectoryFromAPI() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/directory`);
    if (res.ok) {
      const data = await res.json();
      if (data.success && Array.isArray(data.data) && data.data.length >= 10) {
        parentDirectory = data.data.map(item => ({
          rollNo: item.roll_no || item.rollNo,
          studentName: item.student_name || item.studentName,
          department: item.department || "Computer Science",
          year: item.year || 3,
          section: item.section || "3-A",
          parentName: item.parent_name || item.parentName,
          parentPhone: item.parent_phone_number || item.parentPhone,
          advisorId: item.advisor_id || "ADV-MADHAN-01"
        }));
      }
    }
  } catch (err) {
    console.warn("Using local 50 seeded records directory.");
  }
  updateDirectoryStats();
}

async function fetchRequestsFromAPI() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/requests`);
    if (res.ok) {
      const data = await res.json();
      if (data.success && Array.isArray(data.data)) {
        leaveRequests = data.data.map(item => ({
          requestId: item.id || item.request_id || item.requestId || ("REQ-" + Math.floor(Date.now()/1000)),
          rollNo: item.roll_no || item.rollNo,
          studentName: item.student_name || item.studentName || "Student",
          department: item.department || "Computer Science",
          section: item.section || "3-A",
          parentName: item.parent_name || item.parentName || "Parent",
          parentPhone: item.parent_phone || item.parent_phone_number || item.parentPhone,
          type: item.type || item.request_type || "Leave",
          startDate: item.start_date || item.startDate || new Date().toISOString().split('T')[0],
          endDate: item.end_date || item.endDate || new Date().toISOString().split('T')[0],
          durationDays: item.duration_days || item.durationDays || 1,
          reason: item.reason_text || item.reason || "Leave request",
          ivrCallSid: item.call_sid || item.ivr_call_sid || item.ivrCallSid || "",
          recordingUrl: item.audio_url || item.recording_url || item.recordingUrl || "https://api.vapi.ai/recordings/sample.mp3",
          status: item.status || "Pending",
          smsStatus: item.sms_status || item.smsStatus || "⏳ Pending Review",
          advisorNotes: item.advisor_notes || item.advisorNotes || "",
          timestamp: item.received_at ? new Date(item.received_at).toLocaleString() : (item.timestamp || new Date().toLocaleString())
        }));
      }
    }
  } catch (err) {
    console.warn("Using local memory requests.");
  }
  render();
}

function setupEventListeners() {
  document.querySelectorAll(".nav-item").forEach(btn => {
    btn.addEventListener("click", (e) => {
      document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
      const target = e.currentTarget;
      target.classList.add("active");
      activeTab = target.dataset.tab;

      const requestsSection = document.getElementById("requests-section");
      const studentsSection = document.getElementById("students-section");
      const directorySection = document.getElementById("directory-section");

      if (requestsSection) requestsSection.classList.add("hidden");
      if (studentsSection) studentsSection.classList.add("hidden");
      if (directorySection) directorySection.classList.add("hidden");

      if (activeTab === "students") {
        if (studentsSection) studentsSection.classList.remove("hidden");
        document.getElementById("page-title").textContent = "Student Database & Leave/OD Summary";
        document.getElementById("page-subtitle").textContent = "Academic Attendance & Official On-Duty Claim Balances";
        renderStudentsDatabase();
      } else if (activeTab === "directory") {
        if (directorySection) directorySection.classList.remove("hidden");
        document.getElementById("page-title").textContent = "Authorized Parent Database";
        document.getElementById("page-subtitle").textContent = "Caller ID Directory & Linked Student Children Mappings";
        renderDirectory();
      } else {
        if (requestsSection) requestsSection.classList.remove("hidden");
        document.getElementById("page-title").textContent = "Class Advisor Dashboard";
        document.getElementById("page-subtitle").textContent = "Real-time IVR Voice Call Submissions & Direct Approval Engine";
        render();
      }
    });
  });

  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      searchQuery = e.target.value.toLowerCase();
      if (activeTab === "students") {
        renderStudentsDatabase();
      } else if (activeTab === "directory") {
        renderDirectory();
      } else {
        render();
      }
    });
  }

  const filterTypeSelect = document.getElementById("filter-type");
  if (filterTypeSelect) {
    filterTypeSelect.addEventListener("change", (e) => {
      activeFilterType = e.target.value;
      render();
    });
  }

  const btnRefresh = document.getElementById("btn-refresh");
  if (btnRefresh) {
    btnRefresh.addEventListener("click", () => {
      fetchDirectoryFromAPI();
      fetchRequestsFromAPI();
      showToast("Synced with live database!");
    });
  }

  const btnBulkImport = document.getElementById("btn-bulk-import");
  if (btnBulkImport) {
    btnBulkImport.addEventListener("click", () => {
      const modal = document.getElementById("bulk-import-modal");
      if (modal) modal.classList.remove("hidden");
    });
  }

  const bulkCloseBtn = document.getElementById("bulk-close-btn");
  if (bulkCloseBtn) bulkCloseBtn.addEventListener("click", () => document.getElementById("bulk-import-modal").classList.add("hidden"));

  const bulkCancelBtn = document.getElementById("bulk-cancel-btn");
  if (bulkCancelBtn) bulkCancelBtn.addEventListener("click", () => document.getElementById("bulk-import-modal").classList.add("hidden"));

  const btnSaveBulk = document.getElementById("btn-save-bulk");
  if (btnSaveBulk) btnSaveBulk.addEventListener("click", handleSaveBulkCSV);

  const btnWebSip = document.getElementById("btn-web-sip-call");
  if (btnWebSip) {
    btnWebSip.addEventListener("click", () => {
      const sipSelect = document.getElementById("sip-parent-select");
      if (sipSelect) {
        sipSelect.innerHTML = parentDirectory.map(p => 
          `<option value="${p.parentPhone}">📞 ${p.parentName} (${p.parentPhone}) - Ward: ${p.studentName} (${p.rollNo})</option>`
        ).join('');
      }
      document.getElementById("web-sip-modal").classList.remove("hidden");
      
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const greeting = new SpeechSynthesisUtterance("Hello, what is your query? Give information about Leave, OD, or contact the Advisor.");
        window.speechSynthesis.speak(greeting);
      }
    });
  }

  const btnMobileSim = document.getElementById("btn-mobile-sim");
  if (btnMobileSim) {
    btnMobileSim.addEventListener("click", async () => {
      const modal = document.getElementById("mobile-sim-modal");
      if (modal) {
        modal.classList.remove("hidden");
        let pcIp = "127.0.0.1";
        try {
          const res = await fetch(`${API_BASE_URL}/api/get-ip`);
          if (res.ok) {
            const data = await res.json();
            if (data.success && data.ip && data.ip !== "127.0.0.1") {
              pcIp = data.ip;
            }
          }
        } catch(e) {}

        if (pcIp === "127.0.0.1" && window.location.hostname && window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
          pcIp = window.location.hostname;
        }

        const mobileUrl = (pcIp !== "127.0.0.1") ? `http://${pcIp}:3000/mobile.html` : `http://localhost:3000/mobile.html`;
        const qrImg = document.getElementById("mobile-qr-code-img");
        if (qrImg) qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(mobileUrl)}`;
        const linkUrl = document.getElementById("link-mobile-url");
        if (linkUrl) {
          linkUrl.href = mobileUrl;
          linkUrl.textContent = mobileUrl;
        }
      }
    });
  }

  const mobileSimCloseBtn = document.getElementById("mobile-sim-close-btn");
  if (mobileSimCloseBtn) mobileSimCloseBtn.addEventListener("click", () => document.getElementById("mobile-sim-modal").classList.add("hidden"));

  const mobileSimDoneBtn = document.getElementById("mobile-sim-done-btn");
  if (mobileSimDoneBtn) mobileSimDoneBtn.addEventListener("click", () => document.getElementById("mobile-sim-modal").classList.add("hidden"));

  document.querySelectorAll(".dtmf-btn").forEach(btn => {
    btn.addEventListener("click", (e) => {
      const key = e.currentTarget.dataset.key;
      selectedDtmfKey = key;
      playDtmfBeep();

      const stateElem = document.getElementById("sip-call-state");
      const reasonElem = document.getElementById("sip-reason-text");

      if (key === "1") {
        if (stateElem) stateElem.textContent = "DTMF Key 1 Pressed: LEAVE Request Selected";
        if (reasonElem) reasonElem.value = "High fever and viral infection. Doctor prescribed 2 days bed rest.";
        showToast("🔢 DTMF Tone [1] Received: LEAVE Request Selected");
      } else if (key === "2") {
        if (stateElem) stateElem.textContent = "DTMF Key 2 Pressed: ON-DUTY (OD) Request Selected";
        if (reasonElem) reasonElem.value = "Representing college at State Level Robotics Hackathon at IIT.";
        showToast("🔢 DTMF Tone [2] Received: ON-DUTY (OD) Request Selected");
      } else if (key === "3") {
        if (stateElem) stateElem.textContent = "DTMF Key 3 Pressed: Connecting to Prof. Madhan (+91 1800 425 8899)";
        showToast("🔢 DTMF Tone [3] Received: Transferring call to Advisor Prof. Madhan");
        if ('speechSynthesis' in window) {
          window.speechSynthesis.cancel();
          const transferMsg = new SpeechSynthesisUtterance("Connecting your call to Class Advisor Prof. Madhan.");
          window.speechSynthesis.speak(transferMsg);
        }
      }
    });
  });

  const sipCloseBtn = document.getElementById("sip-close-btn");
  if (sipCloseBtn) sipCloseBtn.addEventListener("click", () => document.getElementById("web-sip-modal").classList.add("hidden"));

  const btnExecSip = document.getElementById("btn-execute-sip-call");
  if (btnExecSip) btnExecSip.addEventListener("click", handleExecuteWebSipCall);

  const btnMicListen = document.getElementById("btn-mic-listen");
  if (btnMicListen) {
    btnMicListen.addEventListener("click", toggleMicListening);
  }

  const btnAddParent = document.getElementById("btn-add-parent");
  if (btnAddParent) {
    btnAddParent.addEventListener("click", () => {
      const regModal = document.getElementById("register-parent-modal");
      if (regModal) regModal.classList.remove("hidden");
    });
  }

  const regCloseBtn = document.getElementById("reg-close-btn");
  if (regCloseBtn) regCloseBtn.addEventListener("click", () => document.getElementById("register-parent-modal").classList.add("hidden"));
  
  const regCancelBtn = document.getElementById("reg-cancel-btn");
  if (regCancelBtn) regCancelBtn.addEventListener("click", () => document.getElementById("register-parent-modal").classList.add("hidden"));

  const btnSaveParent = document.getElementById("btn-save-parent");
  if (btnSaveParent) btnSaveParent.addEventListener("click", handleRegisterParent);

  const modalCloseBtn = document.getElementById("modal-close-btn");
  if (modalCloseBtn) modalCloseBtn.addEventListener("click", () => document.getElementById("action-modal").classList.add("hidden"));

  const btnApprove = document.getElementById("btn-modal-approve");
  if (btnApprove) btnApprove.addEventListener("click", () => handleDecision("Approved"));

  const btnReject = document.getElementById("btn-modal-reject");
  if (btnReject) btnReject.addEventListener("click", () => handleDecision("Rejected"));

  const audioCloseBtn = document.getElementById("audio-close-btn");
  if (audioCloseBtn) audioCloseBtn.addEventListener("click", closeAudioModal);

  const audioDoneBtn = document.getElementById("audio-done-btn");
  if (audioDoneBtn) audioDoneBtn.addEventListener("click", closeAudioModal);
}

function handleSaveBulkCSV() {
  const csvText = document.getElementById("bulk-csv-input").value.trim();
  if (!csvText) {
    alert("Please paste CSV data to import.");
    return;
  }

  const lines = csvText.split('\n');
  let addedCount = 0;

  lines.forEach(line => {
    const parts = line.split(',').map(s => s.trim());
    if (parts.length >= 6) {
      const [rollNo, studentName, dept, section, phone, parentName] = parts;
      let formattedPhone = phone;
      if (!formattedPhone.startsWith('+')) {
        formattedPhone = '+' + formattedPhone.replace(/\D/g, '');
      }
      
      const newEntry = {
        rollNo,
        studentName,
        department: dept || "Computer Science",
        year: 3,
        section: section || "3-A",
        parentName: parentName || "Parent",
        parentPhone: formattedPhone,
        advisorId: "ADV-MADHAN-01"
      };

      parentDirectory.unshift(newEntry);
      addedCount++;

      try {
        fetch(`${API_BASE_URL}/api/directory`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            rollNo,
            studentName,
            department: dept,
            year: 3,
            section,
            parentPhone: formattedPhone,
            parentName
          })
        });
      } catch (e) {}
    }
  });

  updateDirectoryStats();
  document.getElementById("bulk-import-modal").classList.add("hidden");
  showToast(`📂 Successfully imported ${addedCount} Parent Directory records into Database!`);

  if (activeTab === "directory") renderDirectory();
  if (activeTab === "students") renderStudentsDatabase();
}

function playDtmfBeep() {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.value = 852;
    gain.gain.value = 0.1;
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    setTimeout(() => { osc.stop(); ctx.close(); }, 150);
  } catch (e) {}
}

function setupSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      document.getElementById("sip-reason-text").value = transcript;
      showToast(`🎙️ Captured Voice: "${transcript}"`);
      document.getElementById("sip-call-state").textContent = "Voice Audio Captured";
    };

    recognition.onerror = (err) => {
      console.warn("Speech recognition error:", err);
    };
  }
}

function toggleMicListening() {
  if (recognition) {
    try {
      recognition.start();
      document.getElementById("sip-call-state").textContent = "🎙️ Listening to Parent Voice Speech...";
      showToast("Speak now into your microphone...");
    } catch (e) {
      recognition.stop();
    }
  } else {
    alert("Speech recognition not supported in this browser. Type your reason in the text box.");
  }
}

function updateDirectoryStats() {
  const countDir = document.getElementById("count-directory");
  if (countDir) countDir.textContent = parentDirectory.length;
  
  const countStud = document.getElementById("count-students");
  if (countStud) countStud.textContent = parentDirectory.length;

  const statReg = document.getElementById("stat-registered-parents");
  if (statReg) statReg.textContent = parentDirectory.length;
}

async function handleExecuteWebSipCall() {
  const selectedPhone = document.getElementById("sip-parent-select").value;
  const reasonText = document.getElementById("sip-reason-text").value.trim() || "High fever and doctor advised 2 days bed rest.";
  
  document.getElementById("sip-call-state").textContent = "Transmitting Request to n8n & Dashboard...";
  
  const todayStr = new Date().toISOString().split('T')[0];
  const matchedParent = parentDirectory.find(p => p.parentPhone === selectedPhone) || parentDirectory[0];

  const newReqId = "REQ-" + strTimestamp();
  const newCallSid = "AST-DTMF-" + strTimestamp();

  const isOD = selectedDtmfKey === "2" || reasonText.toLowerCase().includes("od") || reasonText.toLowerCase().includes("duty") || reasonText.toLowerCase().includes("hackathon") || reasonText.toLowerCase().includes("competition");

  const newRequestObj = {
    requestId: newReqId,
    rollNo: matchedParent.rollNo,
    studentName: matchedParent.studentName,
    department: matchedParent.department,
    section: matchedParent.section,
    parentName: matchedParent.parentName,
    parentPhone: matchedParent.parentPhone,
    type: isOD ? "OD" : "Leave",
    startDate: todayStr,
    endDate: todayStr,
    durationDays: isOD ? 1 : 2,
    reason: reasonText,
    ivrCallSid: newCallSid,
    recordingUrl: "https://api.vapi.ai/recordings/asterisk-web.mp3",
    status: "Pending",
    advisorNotes: "",
    timestamp: new Date().toLocaleString()
  };

  leaveRequests.unshift(newRequestObj);
  render();

  const payload = {
    message: {
      customer: { number: selectedPhone },
      call: { id: newCallSid },
      recordingUrl: "https://api.vapi.ai/recordings/asterisk-web.mp3",
      toolCalls: [
        {
          function: {
            name: "submitLeaveODRequest",
            arguments: {
              requestType: isOD ? "OD" : "Leave",
              startDate: todayStr,
              endDate: todayStr,
              durationDays: isOD ? 1 : 2,
              reason: reasonText
            }
          }
        }
      ]
    }
  };

  try {
    await fetch(`${API_BASE_URL}/api/webhook/vapi-end-call`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  } catch (e) {
    console.warn("Local API offline, processed via in-memory workflow pipeline.");
  }

  showToast(`📞 Asterisk DTMF Call Completed! Logged as ${newReqId} for Prof. Madhan Review.`);
  document.getElementById("web-sip-modal").classList.add("hidden");
  document.getElementById("sip-call-state").textContent = "Asterisk IVR Greeting Connected";
}

function strTimestamp() {
  return Math.floor(Date.now() / 1000).toString();
}

function renderStudentsDatabase() {
  const studentsTbody = document.getElementById("students-tbody");
  if (!studentsTbody) return;

  studentsTbody.innerHTML = "";

  let filtered = parentDirectory.filter(p => {
    if (!searchQuery) return true;
    return p.studentName.toLowerCase().includes(searchQuery) ||
           p.rollNo.toLowerCase().includes(searchQuery) ||
           p.department.toLowerCase().includes(searchQuery);
  });

  filtered.forEach(student => {
    const studentRequests = leaveRequests.filter(r => r.rollNo === student.rollNo);
    const leaveCount = studentRequests.filter(r => r.type === "Leave" && r.status === "Approved").reduce((sum, r) => sum + (r.durationDays || 1), 0);
    const odCount = studentRequests.filter(r => r.type === "OD" && r.status === "Approved").reduce((sum, r) => sum + (r.durationDays || 1), 0);

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><strong class="text-primary">${student.rollNo}</strong></td>
      <td><strong>${student.studentName}</strong></td>
      <td>${student.department} (Year ${student.year || 3})</td>
      <td><span class="badge warning">${student.section}</span></td>
      <td><span class="badge danger" style="font-size: 0.85rem; padding: 6px 12px;">🔴 ${leaveCount} Days Leave</span></td>
      <td><span class="badge info" style="font-size: 0.85rem; padding: 6px 12px;">🏅 ${odCount} Days OD</span></td>
      <td>🛡️ ${student.parentName} (${student.parentPhone})</td>
      <td><span class="badge success">${student.advisorId || 'ADV-MADHAN-01'}</span></td>
      <td class="text-right">
        <button class="btn btn-danger" style="padding: 6px 12px; font-size: 0.75rem;" onclick="removeParent('${student.rollNo}')">
          Remove Data
        </button>
      </td>
    `;
    studentsTbody.appendChild(tr);
  });
}

function renderDirectory() {
  const directoryTbody = document.getElementById("directory-tbody");
  const directoryEmptyState = document.getElementById("directory-empty-state");
  if (!directoryTbody) return;

  directoryTbody.innerHTML = "";

  let filtered = parentDirectory.filter(p => {
    if (!searchQuery) return true;
    return p.studentName.toLowerCase().includes(searchQuery) ||
           p.rollNo.toLowerCase().includes(searchQuery) ||
           p.parentPhone.toLowerCase().includes(searchQuery) ||
           p.parentName.toLowerCase().includes(searchQuery);
  });

  if (filtered.length === 0) {
    if (directoryEmptyState) directoryEmptyState.classList.remove("hidden");
  } else {
    if (directoryEmptyState) directoryEmptyState.classList.add("hidden");
    filtered.forEach(p => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong class="text-primary">${p.rollNo}</strong></td>
        <td><strong>${p.studentName}</strong></td>
        <td>${p.department} (${p.section})</td>
        <td>🛡️ <strong>${p.parentName}</strong></td>
        <td><span class="caller-id-badge" style="font-family: monospace; font-size: 0.9rem;">📞 ${p.parentPhone}</span></td>
        <td><span class="badge success">✅ AUTHORIZED CALLER ID</span></td>
        <td class="text-right">
          <button class="btn btn-danger" style="padding: 6px 12px; font-size: 0.75rem;" onclick="removeParent('${p.rollNo}')">
            Remove Data
          </button>
        </td>
      `;
      directoryTbody.appendChild(tr);
    });
  }
}

async function handleRegisterParent() {
  const rollNo = document.getElementById("reg-roll-no").value.trim();
  const studentName = document.getElementById("reg-student-name").value.trim();
  const dept = document.getElementById("reg-dept").value;
  const section = document.getElementById("reg-section").value.trim() || "A";
  const parentName = document.getElementById("reg-parent-name").value.trim();
  let parentPhone = document.getElementById("reg-parent-phone").value.trim();

  if (!rollNo || !studentName || !parentName || !parentPhone) {
    alert("Please fill in all fields (Roll No, Student Name, Parent Name, and Parent Phone Number).");
    return;
  }

  if (!parentPhone.startsWith("+")) {
    parentPhone = "+" + parentPhone.replace(/\D/g, "");
  }

  const newEntry = {
    rollNo,
    studentName,
    department: dept,
    year: 3,
    section,
    parentName,
    parentPhone,
    advisorId: "ADV-MADHAN-01"
  };

  parentDirectory.unshift(newEntry);
  updateDirectoryStats();

  try {
    await fetch(`${API_BASE_URL}/api/directory`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rollNo,
        studentName,
        department: dept,
        year: 3,
        section,
        parentPhone,
        parentName
      })
    });
  } catch (e) {
    console.warn("Local API offline, parent saved to memory directory.");
  }

  document.getElementById("reg-roll-no").value = "";
  document.getElementById("reg-student-name").value = "";
  document.getElementById("reg-parent-name").value = "";
  document.getElementById("reg-parent-phone").value = "";
  document.getElementById("register-parent-modal").classList.add("hidden");

  showToast(`Authorized parent number ${parentPhone} for student ${studentName}!`);
  
  if (activeTab === "directory") {
    renderDirectory();
  } else if (activeTab === "students") {
    renderStudentsDatabase();
  }
}

async function removeParent(rollNo) {
  if (!confirm(`Are you sure you want to remove all data for Roll No: ${rollNo}?`)) {
    return;
  }

  parentDirectory = parentDirectory.filter(p => p.rollNo.toLowerCase() !== rollNo.toLowerCase());
  leaveRequests = leaveRequests.filter(r => r.rollNo.toLowerCase() !== rollNo.toLowerCase());

  updateDirectoryStats();

  try {
    await fetch(`${API_BASE_URL}/api/directory/${encodeURIComponent(rollNo)}`, {
      method: "DELETE"
    });
  } catch (e) {
    console.warn("Local API offline, removed from memory state.");
  }

  showToast(`Removed data for Roll No: ${rollNo}`);

  if (activeTab === "directory") {
    renderDirectory();
  } else if (activeTab === "students") {
    renderStudentsDatabase();
  } else {
    render();
  }
}

function render() {
  const tbody = document.getElementById("requests-tbody");
  const emptyState = document.getElementById("empty-state");
  if (!tbody) return;

  let filtered = leaveRequests.filter(req => {
    if (activeTab === "pending" && req.status !== "Pending") return false;
    if (activeTab === "approved" && req.status !== "Approved") return false;
    if (activeTab === "rejected" && req.status !== "Rejected") return false;

    if (activeFilterType !== "ALL" && req.type !== activeFilterType) return false;

    if (searchQuery) {
      const matchName = req.studentName.toLowerCase().includes(searchQuery);
      const matchRoll = req.rollNo.toLowerCase().includes(searchQuery);
      const matchReason = req.reason.toLowerCase().includes(searchQuery);
      const matchPhone = req.parentPhone.toLowerCase().includes(searchQuery);
      if (!matchName && !matchRoll && !matchReason && !matchPhone) return false;
    }

    return true;
  });

  const countPending = leaveRequests.filter(r => r.status === "Pending").length;

  const cntPending = document.getElementById("count-pending");
  if (cntPending) cntPending.textContent = countPending;
  
  const cntAll = document.getElementById("count-all");
  if (cntAll) cntAll.textContent = leaveRequests.length;

  const cntApp = document.getElementById("count-approved");
  if (cntApp) cntApp.textContent = leaveRequests.filter(r => r.status === "Approved").length;

  const cntRej = document.getElementById("count-rejected");
  if (cntRej) cntRej.textContent = leaveRequests.filter(r => r.status === "Rejected").length;

  const statPending = document.getElementById("stat-pending");
  if (statPending) statPending.textContent = countPending;

  const statApp = document.getElementById("stat-approved");
  if (statApp) statApp.textContent = leaveRequests.filter(r => r.status === "Approved").length;

  tbody.innerHTML = "";
  if (filtered.length === 0) {
    if (emptyState) emptyState.classList.remove("hidden");
  } else {
    if (emptyState) emptyState.classList.add("hidden");
    filtered.forEach(req => {
      const tr = document.createElement("tr");

      const statusBadgeClass = 
        req.status === "Approved" ? "badge success" :
        req.status === "Rejected" ? "badge danger" : "badge warning";

      const statusBadgeText = 
        req.status === "Approved" ? "Approved" :
        req.status === "Rejected" ? "Rejected" : "⏳ Pending Review";

      const typeBadgeClass = req.type === "OD" ? "badge info" : "badge warning";
      const escapedReason = req.reason.replace(/'/g, "\\'");

      const smsStatusBadge = req.status === "Pending" 
        ? `<span class="badge warning" style="font-size:0.75rem;">⏳ Pending Review</span>`
        : `<span class="badge success" style="font-size:0.75rem;">📩 SMS Delivered</span>`;

      tr.innerHTML = `
        <td><strong class="text-primary">${req.requestId}</strong><br><span class="text-muted" style="font-size:0.75rem;">${req.timestamp}</span></td>
        <td>
          <div class="student-info">
            <h5>${req.studentName}</h5>
            <p>${req.rollNo} • ${req.department} (${req.section})</p>
          </div>
        </td>
        <td><span class="${typeBadgeClass}">${req.type}</span></td>
        <td>
          <strong>${req.startDate}</strong> to <strong>${req.endDate}</strong><br>
          <span class="text-muted" style="font-size:0.8rem;">${req.durationDays} Day(s)</span>
        </td>
        <td>
          <div class="reason-quote">"${req.reason}"</div>
          <div class="audio-chip" onclick="playAudio('${req.ivrCallSid}', '${escapedReason}', '${req.recordingUrl}')">
            🔊 Listen Recording (${req.ivrCallSid})
          </div>
        </td>
        <td>
          <div class="caller-id-badge">
            🛡️ ${req.parentName}<br>
            <span class="text-muted" style="font-size:0.75rem;">${req.parentPhone}</span>
          </div>
        </td>
        <td><span class="${statusBadgeClass}">${statusBadgeText}</span></td>
        <td>${smsStatusBadge}</td>
        <td class="text-right">
          ${req.status === "Pending" ? `
            <button class="btn btn-primary" onclick="openActionModal('${req.requestId}')">
              Review Action
            </button>
          ` : `
            <span class="text-muted" style="font-size:0.8rem;">Reviewed</span>
          `}
        </td>
      `;
      tbody.appendChild(tr);
    });
  }
}

function openActionModal(requestId) {
  selectedRequestId = requestId;
  const req = leaveRequests.find(r => r.requestId === requestId);
  if (!req) return;

  document.getElementById("modal-student-name").textContent = req.studentName;
  document.getElementById("modal-roll-no").textContent = req.rollNo;
  document.getElementById("modal-type-badge").textContent = `${req.type} • ${req.durationDays} Days`;
  document.getElementById("modal-parent-info").textContent = `${req.parentName} (${req.parentPhone})`;
  document.getElementById("modal-reason").textContent = req.reason;
  document.getElementById("modal-notes").value = "";

  document.getElementById("action-modal").classList.remove("hidden");
}

async function handleDecision(newStatus) {
  if (!selectedRequestId) return;
  const req = leaveRequests.find(r => r.requestId === selectedRequestId);
  if (req) {
    const notes = document.getElementById("modal-notes").value || (newStatus === "Approved" ? "Approved by Class Advisor" : "Rejected by Class Advisor");
    req.status = newStatus;
    req.advisorNotes = notes;

    document.getElementById("action-modal").classList.add("hidden");
    render();

    if (activeTab === "students") {
      renderStudentsDatabase();
    }

    try {
      await fetch(`${API_BASE_URL}/api/requests/${req.requestId}/action`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus, advisorNotes: notes })
      });
    } catch (e) {
      console.warn("Local API offline, decision saved to memory.");
    }

    showToast(`Request ${newStatus}! n8n sent decision notification to parent ${req.parentPhone}.`);
  }
}

function playAudio(callSid, reason, recordingUrl) {
  document.getElementById("audio-title").textContent = `Call SID: ${callSid}`;
  const audioElement = document.getElementById("html5-audio-player");
  const ttsBox = document.getElementById("tts-fallback-box");

  document.getElementById("audio-modal").classList.remove("hidden");

  if (recordingUrl && recordingUrl.endsWith(".mp3") && !recordingUrl.includes("sample-")) {
    audioElement.src = recordingUrl;
    ttsBox.classList.add("hidden");
    audioElement.play().catch(() => playSpeechFallback(reason));
  } else {
    audioElement.src = "";
    ttsBox.classList.remove("hidden");
    playSpeechFallback(reason);
  }
}

function playSpeechFallback(reasonText) {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      `Transcribed IVR Call Reason for Class Advisor: ${reasonText}`
    );
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  }
}

function closeAudioModal() {
  document.getElementById("audio-modal").classList.add("hidden");
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  const audioElement = document.getElementById("html5-audio-player");
  audioElement.pause();
}

function showToast(msg) {
  const toast = document.createElement("div");
  toast.style.position = "fixed";
  toast.style.bottom = "24px";
  toast.style.right = "24px";
  toast.style.background = "#6366f1";
  toast.style.color = "#fff";
  toast.style.padding = "14px 20px";
  toast.style.borderRadius = "10px";
  toast.style.boxShadow = "0 10px 25px rgba(0,0,0,0.5)";
  toast.style.zIndex = "2000";
  toast.style.fontWeight = "600";
  toast.style.fontSize = "0.9rem";
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}
