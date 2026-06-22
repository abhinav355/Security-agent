import os
import hashlib
from datetime import datetime

SUSPICIOUS_EXTENSIONS = {
    ".bat", ".cmd", ".ps1", ".vbs", ".js", ".hta", ".scr", ".exe"
}

SUSPICIOUS_WORDS = {
    "crack", "keygen", "hack", "patch",
    "loader", "inject", "bypass",
    "activate", "free", "update"
}

IGNORE_PATHS = [
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "AppData\\Local\\Programs\\Python"
]

SCAN_PATHS = [
    os.path.expanduser("~/Desktop"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/AppData/Local/Temp"),
    os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
]


def sha256(path):
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                h.update(chunk)
        return h.hexdigest()
    except:
        return "Unknown"


def calculate_risk(name, ext, path):
    score = 0

    if ext in SUSPICIOUS_EXTENSIONS:
        score += 20

    for word in SUSPICIOUS_WORDS:
        if word in name.lower():
            score += 35

    if "downloads" in path.lower():
        score += 15

    if "temp" in path.lower():
        score += 20

    if "startup" in path.lower():
        score += 40

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def scan_computer():

    results = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_found": 0,
        "files_found": []
    }

    for folder in SCAN_PATHS:

        if not os.path.exists(folder):
            continue

        for root, dirs, files in os.walk(folder):

            if any(x.lower() in root.lower() for x in IGNORE_PATHS):
                continue

            for file in files:

                ext = os.path.splitext(file)[1].lower()

                if ext not in SUSPICIOUS_EXTENSIONS:
                    continue

                full_path = os.path.join(root, file)

                risk_score, risk_level = calculate_risk(
                    file,
                    ext,
                    full_path
                )

                results["files_found"].append({
                    "name": file,
                    "path": full_path,
                    "type": ext,
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "sha256": sha256(full_path)
                })

    results["total_found"] = len(results["files_found"])

    return results