# 🛡️ Security Agent (change this if u want to)

A lightweight desktop security tool built with **Python** and **PyWebView**.

Security Agent helps identify files that may deserve a closer look by using two different scanning methods:

* 📁 **File Scanner** – Looks for potentially risky executable and script files.
* 🔍 **Threat Name Scanner** – Searches filenames for known malware and hacking-tool names.

The project was built to learn more about desktop development, file scanning, hashing, and basic security concepts while creating an application with a clean desktop interface.

---

# ✨ Features

## 📁 File Scanner

Scans common user folders such as:

* Desktop
* Downloads
* Documents
* Temp
* Startup Folder

Looks for file types including:

* `.exe`
* `.bat`
* `.cmd`
* `.ps1`
* `.vbs`
* `.js`
* `.hta`
* `.scr`

Each detected file is assigned a **risk score** based on several factors:

* File extension
* Filename
* File location
* Startup folder detection
* Temporary folder detection

For every detected file, the scanner also calculates a **SHA-256 hash** for identification.

---

## 🔍 Threat Name Scanner

This scanner compares filenames against a built-in database of known malware families and security tools.

Examples include:

* Emotet
* TrickBot
* RedLine
* Vidar
* LockBit
* Lumma
* AsyncRAT
* NanoCore
* Mimikatz

If a filename matches one or more keywords, it is added to the scan results along with a calculated risk level.

`.msi` installer files are also flagged for manual review.

---

# 🖥️ Interface

The desktop application is built using **PyWebView**, allowing Python to communicate with a modern HTML, CSS and JavaScript interface.

The interface includes:

* Modern home screen
* Multiple scanning modules
* Scan progress animation
* Risk indicators
* Detailed scan results
* About page

---

# 🛠️ Built With

* Python
* HTML
* CSS
* JavaScript
* PyWebView

---

# 📂 Project Structure

```text
Security-Agent/
│
├── function.py          # Starts the application
├── UI.html              # Desktop interface
├── pc_scan_one.py       # File Scanner
├── RNF_SCAN.py          # Threat Name Scanner
├── RNF.txt              # Threat keyword database
└── README.md
```

---

# ⚙️ How It Works

```text
Launch Application
        │
        ▼
Choose Scanner
        │
        ▼
Scan Files
        │
        ▼
Calculate Risk
        │
        ▼
Generate SHA-256 Hashes
        │
        ▼
Display Results
```

---

# 🎯 Why I Built This

I wanted to explore how desktop security utilities work and learn more about Python desktop applications.

Instead of creating a command-line program, I built a graphical desktop application that separates different scanners into individual modules. This made it easier to organize the project while learning about file scanning, hashing, risk scoring, and frontend/backend communication using PyWebView.

---

# 🚀 Future Improvements

Some ideas I'd like to work on in future versions:

* Process Scanner
* Startup Manager
* Network Monitor
* File Reputation Checker
* Scan History
* Export Scan Reports
* Additional Detection Modules

---

# ⚠️ Disclaimer

Security Agent is a ummm a (goood thing(❁´◡`❁))

It uses filename analysis, file extensions, folder locations and simple heuristics to identify files that may require further inspection.
