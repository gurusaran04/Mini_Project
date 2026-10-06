/**
 * n8n JavaScript Function Node: Validate Caller ID & Match Student Directory
 * Checks if DB query returned a matching parent-student directory record.
 */

// $input.all() receives results from PostgreSQL/Airtable DB Lookup Node
const parsedCall = $('Parse Vapi Payload').first().json;
const dbMatch = $input.all()[0]?.json;

if (!dbMatch || !dbMatch.roll_no) {
  // Fraud/Unregistered Caller Detected
  return [{
    json: {
      isValidCaller: false,
      error: "UNAUTHORIZED_CALLER_ID",
      callerPhone: parsedCall.callerPhone,
      message: `Call received from unregistered number ${parsedCall.callerPhone}. Request rejected automatically.`,
      alertAdmin: true
    }
  }];
}

// Successful Authentication Match
return [{
  json: {
    isValidCaller: true,
    rollNo: dbMatch.roll_no,
    studentName: dbMatch.student_name,
    department: dbMatch.department,
    year: dbMatch.year,
    section: dbMatch.section,
    parentName: dbMatch.parent_name,
    parentPhone: dbMatch.parent_phone_number,
    advisorId: dbMatch.advisor_id,
    advisorEmail: dbMatch.advisor_email || "advisor@institution.edu",
    advisorPhone: dbMatch.advisor_phone || "+15550192831",
    // Passed Request Metadata
    requestType: parsedCall.requestType,
    startDate: parsedCall.startDate,
    endDate: parsedCall.endDate,
    durationDays: parsedCall.durationDays,
    reason: parsedCall.reason,
    callSid: parsedCall.callSid,
    recordingUrl: parsedCall.recordingUrl
  }
}];
