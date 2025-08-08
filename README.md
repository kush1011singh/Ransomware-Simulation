# 🛡️ Ransomware Simulation – Safe & Controlled Offensive Security Project

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Security-Red%20Team-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)
![License](https://img.shields.io/badge/License-Educational-lightgrey.svg)

> ⚠️ **Educational Use Only** – This is a safe, reversible ransomware simulation project intended for **cybersecurity training** and **portfolio demonstration**.  
> No real encryption is performed, and the project is 100% lab-safe.

---

## 📖 Table of Contents
- [About the Project](#about-the-project)
- [Why This Project Matters](#why-this-project-matters)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Lab Environment Setup](#lab-environment-setup)
- [Attack Lifecycle Simulation](#attack-lifecycle-simulation)
- [Detailed Workflow](#detailed-workflow)
- [Usage Instructions](#usage-instructions)
- [Sample Output](#sample-output)
- [Defensive Insights](#defensive-insights)
- [Future Enhancements](#future-enhancements)
- [Author](#author)
- [Legal Disclaimer](#legal-disclaimer)

---

## 💡 About the Project
This project replicates the **behavior of modern ransomware** in a safe, controlled lab.  
It is designed to:
- Showcase **red team attack simulation skills**.
- Demonstrate **malware behavior analysis**.
- Train defenders in **incident response** without any real-world risk.

Unlike real ransomware, this simulation:
- **Does not encrypt** file contents.
- Only **renames** files with a `.locked` extension.
- Generates a **fake ransom note** for realism.
- Keeps a **manifest** of changes to allow full restoration.

---

## 🚀 Why This Project Matters
Recruiters and security leads look for **practical, demonstrable skills** — not just theory.  
By including this project in your portfolio, you’re showing that you can:
- Design and run realistic **attack chain simulations**.
- Work in **isolated, safe environments**.
- Document findings in **professional security reports**.
- Understand both **offensive tactics** and **defensive countermeasures**.

**MITRE ATT&CK Reference:**  
> **T1486 – Data Encrypted for Impact**

---

## ✨ Features
✅ Safe ransomware simulation (no real encryption)  
✅ Creates dummy files for testing  
✅ Simulates file encryption by renaming  
✅ Generates a fake ransom note  
✅ Tracks all changes in a JSON manifest  
✅ Allows full restoration of original files  
✅ Works cross-platform in lab environments  

---

## 🛠 Technology Stack
- **Language:** Python 3
- **Visualization:** [draw.io](https://app.diagrams.net/)
- **Environment:** VirtualBox / VMware
- **Version Control:** GitHub
- **Reporting:** PDF via ReportLab

---

## 🏗 Lab Environment Setup
| Component        | Description |
|------------------|-------------|
| **Attacker**     | Kali Linux 2024 with Python 3 |
| **Victim**       | Windows 10 Pro (VM) / Ubuntu Linux |
| **Virtualization** | VirtualBox with host-only network |
| **Safety**       | No internet, dummy files only |

<details>
<summary>🔧 Setup Steps (Click to Expand)</summary>

1. Install VirtualBox or VMware.  
2. Create two VMs (Kali Linux + Victim OS).  
3. Disable network access to prevent accidental spread.  
4. Clone this repo inside the victim VM.  
</details>

---

## 🎯 Attack Lifecycle Simulation

[Initial Access]
↓
[File Discovery]
↓
[Simulated Encryption]
↓
[Ransom Note Dropped]
↓
[Manifest Recorded]
↓
[Restoration]


---

## 🔍 Detailed Workflow
<details>
<summary>📜 Step-by-Step Process</summary>

### **1. File Discovery**
- Scans target directory for files to “encrypt.”
- Ignores manifest and ransom note.

### **2. Simulated Encryption**
- Appends `.locked` to filenames.
- Example: `report.docx` → `report.docx.locked`.

### **3. Ransom Note Creation**
- Drops `README_RESTORE_FILES.txt` with fake payment instructions.

### **4. Manifest Recording**
- `.ransomware_manifest.json` logs:
  - Original filename
  - Locked filename
  - Timestamp
  - Session ID

### **5. Restoration Process**
- Using `--restore` flag, files are returned to original state.
- Ransom note is deleted.
</details>

---

## 💻 Usage Instructions
```bash
# Create dummy files
python3 ransomware_simulation.py --target test_files --create

# Simulate ransomware attack
python3 ransomware_simulation.py --target test_files

# Restore original files
python3 ransomware_simulation.py --target test_files --restore

```
📸 Sample Output
Terminal Output:

```bash
Simulation complete. 3 file(s) renamed. Manifest updated.
```
Folder View (After Simulation):
```
file1.txt.locked
file2.txt.locked
file3.txt.locked
README_RESTORE_FILES.txt
.ransomware_manifest.json
```
Folder View (After Restore):
```
file1.txt
file2.txt
file3.txt
```
🛡 Defensive Insights
->From this simulation, defenders learn:

->Detect unusual file renaming at scale.

->Monitor creation of suspicious .txt ransom notes.

->Implement file integrity monitoring (FIM).

->Train staff to avoid executing unknown scripts.


🔮 Future Enhancements
Add simulated Command & Control (C2) for beacons.

->Simulate data exfiltration.

->Log events for SIEM integration.

->Multi-threaded “encryption” for realism.

👨‍💻 Author
Name: Kushagra Patel

Role: Cybersecurity & Red Team Enthusiast

LinkedIn: https://www.linkedin.com/in/kushagra-patel/


⚠️ Legal Disclaimer

This simulation is intended solely for educational purposes inside an isolated lab.
Running it on real systems or without permission is illegal and unethical.
