# 📱 ZoiPer Softphone Setup Guide for Asterisk PBX

This guide explains how to connect **ZoiPer Softphone** (Desktop for Windows/Mac or Mobile for Android/iOS) to your Dockerized **Asterisk PBX System** on UDP/TCP port `5060`.

---

### ⚙️ ZoiPer Extension Credentials

Use these credentials to register ZoiPer softphones to your Asterisk PBX:

| Extension | Role | Username | Password | Domain / Host | Transport |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1001** | Student / Parent Softphone | `1001` | `password1001` | `127.0.0.1:5060` | `UDP` |
| **1002** | Faculty Advisor (Prof. Madhan) | `1002` | `password1002` | `127.0.0.1:5060` | `UDP` |

---

### 🚀 Step-by-Step ZoiPer Desktop / Mobile Configuration:

#### **Step 1: Open ZoiPer & Add Account**
1. Launch **ZoiPer**.
2. Click **Settings ⚙️** → **Accounts** → **Add Account (+)**.
3. Select **SIP** account type.

#### **Step 2: Enter SIP Credentials**
- **Domain / Host**: `127.0.0.1:5060` *(or your PC's IP e.g. `192.168.1.5:5060` if using ZoiPer Mobile over Wi-Fi)*
- **Username / User ID**: `1001` *(for Parent)* or `1002` *(for Faculty)*
- **Password**: `password1001` *(for 1001)* or `password1002` *(for 1002)*
- **Caller ID / Display Name**: `Parent Softphone` or `Prof. Madhan`
- **Transport**: `UDP` (or `TCP`)

#### **Step 3: Save & Register**
- Click **Register / Save**.
- ZoiPer status will turn **🟢 Account is online!**

---

### 📞 Testing IVR Dialplan & Calls via ZoiPer:

1. **Dial `1000` or `18004258899`**:
   - Triggers Asterisk Custom IVR Menu:
     > *"Press 1 for Leave, Press 2 for On-Duty, or Press 3 for Direct Interaction with the Faculty."*
2. **Press DTMF `1`**:
   - Plays confirmation message (*"Connecting to the attendance department"*) and routes call.
3. **Press DTMF `2`**:
   - Plays confirmation message (*"Connecting to the On-Duty coordination desk"*) and routes call.
4. **Press DTMF `3`**:
   - Directly rings **Faculty Extension 1002** (Prof. Madhan's ZoiPer softphone rings live!).
