/**
 * n8n JavaScript Function Node: Parse Vapi.ai / Retell Webhook Payload
 * Handles call metadata, tool call arguments, call SID, recording URL, and caller phone number.
 */

// Retrieve input item from n8n trigger node
const body = $json.body || $json;

// Extract core fields from Vapi payload structure
let callerPhone = body.message?.customer?.number || body.call?.customer?.number || body.caller_id || "";
let callSid = body.message?.call?.id || body.call?.id || "CALL-" + Date.now();
let recordingUrl = body.message?.recordingUrl || body.recording_url || "";
let callDuration = body.message?.durationSeconds || body.duration_seconds || 0;

// Extract function arguments from Vapi tool call or end-of-call report
let functionArgs = {};

if (body.message?.type === "tool-calls" && body.message?.toolCalls?.length > 0) {
  functionArgs = body.message.toolCalls[0].function.arguments || {};
} else if (body.message?.analysis?.structuredData) {
  functionArgs = body.message.analysis.structuredData;
} else if (body.function_arguments) {
  functionArgs = body.function_arguments;
} else {
  // Direct fallback
  functionArgs = {
    parentPhoneNumber: callerPhone,
    requestType: body.requestType || "Leave",
    startDate: body.startDate || new Date().toISOString().split('T')[0],
    endDate: body.endDate || new Date().toISOString().split('T')[0],
    durationDays: body.durationDays || 1,
    reason: body.reason || "Not specified"
  };
}

// Clean phone number format to standard E.164
if (callerPhone && !callerPhone.startsWith('+')) {
  callerPhone = '+' + callerPhone.replace(/\D/g, '');
}

return [{
  json: {
    callerPhone: callerPhone,
    callSid: callSid,
    recordingUrl: recordingUrl,
    callDurationSeconds: callDuration,
    requestType: functionArgs.requestType || "Leave",
    startDate: functionArgs.startDate,
    endDate: functionArgs.endDate,
    durationDays: parseInt(functionArgs.durationDays) || 1,
    reason: functionArgs.reason || "Voice IVR submission",
    parsedAt: new Date().toISOString()
  }
}];
