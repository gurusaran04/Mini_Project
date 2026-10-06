/**
 * n8n JavaScript Function Node: Format SMS / WhatsApp Parent Notification Payload
 * Builds dynamic template body for Twilio SMS / WhatsApp API dispatch.
 */

const item = $json;
const status = item.status || "Pending";
const studentName = item.student_name || item.studentName || "your ward";
const rollNo = item.roll_no || item.rollNo || "";
const requestType = item.request_type || item.requestType || "Leave";
const startDate = item.start_date || item.startDate;
const endDate = item.end_date || item.endDate;
const advisorNotes = item.advisor_notes || item.advisorNotes || "None";
const parentPhone = item.parent_phone_number || item.parentPhone;

let messageText = "";

if (status === "Approved") {
  messageText = `✅ OFFICIAL INSTITUTION NOTICE: The ${requestType} request for ${studentName} (${rollNo}) from ${startDate} to ${endDate} has been APPROVED by the Class Advisor.\nAdvisor Remarks: "${advisorNotes}".\nThank you for utilizing the IVR portal.`;
} else if (status === "Rejected") {
  messageText = `❌ OFFICIAL INSTITUTION NOTICE: The ${requestType} request for ${studentName} (${rollNo}) from ${startDate} to ${endDate} has been REJECTED by the Class Advisor.\nReason/Remarks: "${advisorNotes}".\nPlease contact the department for further clarification.`;
} else {
  messageText = `📋 ACKNOWLEDGEMENT: We have received your voice call request for ${studentName} (${rollNo}) for ${requestType} (${startDate} to ${endDate}). Status: PENDING ADVISOR REVIEW. You will receive an automated alert upon decision.`;
}

return [{
  json: {
    to: parentPhone,
    from: "whatsapp:+14155238886", // Twilio WhatsApp sandbox number or Twilio SMS number
    body: messageText,
    studentRollNo: rollNo,
    status: status,
    timestamp: new Date().toISOString()
  }
}];
