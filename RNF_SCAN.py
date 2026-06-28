import os
import re
import hashlib
from datetime import datetime

#ill add morefoler to skip later or anyone change it
IGNORE_DIR_NAMES = [
    "windows",
    "program files",
    "program files (x86)",
    "appdata\\local\\programs\\python",
    "node_modules",
    ".git",
]


def _script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def load_keywords(domain_file=None):
    if domain_file is None:
        domain_file = os.path.join(_script_dir(), "RNF.txt")

    if not os.path.exists(domain_file):
        print(f"[-] Error: Could not find keyword file: {domain_file}")
        return []

    with open(domain_file, "r", encoding="utf-8") as file:
        return [line.strip().lower() for line in file if line.strip()]


def _normalize(text):
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _tokenize(name_no_ext):
    return [t for t in re.split(r"[ _\-.]+", name_no_ext.lower()) if t]


def find_matches(name_no_ext, keywords):
    tokens = _tokenize(name_no_ext)
    normalized_full = _normalize(name_no_ext)

    matches = []
    for term in keywords:
        if " " in term:
            normalized_term = _normalize(term)
            if normalized_term and normalized_term in normalized_full:
                matches.append(term)
        else:
            if term in tokens or (term + "s") in tokens:
                matches.append(term)
    return matches


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
    except OSError:
        return "Unknown"


def calculate_risk(matched_terms, ext, path):
    score = 0

    if matched_terms:
        score += 50
        if len(matched_terms) > 1:
            score += 15

    if ext == ".msi":
        score += 15

    path_lower = path.lower()
    if "downloads" in path_lower:
        score += 15
    if "temp" in path_lower:
        score += 20
    if "startup" in path_lower:
        score += 40

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


def get_scan_directory():
    return os.path.expanduser("~")


def scan_rnf(scan_path=None, domain_file=None):
    keywords = load_keywords(domain_file)

    if scan_path is None:
        scan_path = get_scan_directory()

    results = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_found": 0,
        "files_found": [],
    }

    if not keywords or not os.path.exists(scan_path):
        return results

    for root, dirs, files in os.walk(scan_path):
        root_lower = root.lower()
        if any(ignored in root_lower for ignored in IGNORE_DIR_NAMES):
            dirs[:] = []
            continue

        for filename in files:
            name_no_ext, ext = os.path.splitext(filename)
            ext = ext.lower()
            full_path = os.path.join(root, filename)

            matched_terms = find_matches(name_no_ext, keywords)
            is_msi = ext == ".msi"

            if not matched_terms and not is_msi:
                continue

            risk_score, risk_level = calculate_risk(matched_terms, ext, full_path)

            results["files_found"].append({
                "name": filename,
                "path": full_path,
                "type": ext if ext else "(none)",
                "match_reason": ", ".join(matched_terms) if matched_terms else "MSI installer",
                "risk_score": risk_score,
                "risk_level": risk_level,
                "sha256": sha256(full_path),
            })

    results["total_found"] = len(results["files_found"])
    return results


if __name__ == "__main__":
    OUTPUT_FILE = "scan_results.txt"

    target_keywords = load_keywords()

    if target_keywords:
        scan_dir = get_scan_directory()
        print(f"[*] Starting scan in user directory: {scan_dir}")
        print(f"[*] Checking for '.msi' files and {len(target_keywords)} known threat names/keywords...")

        scan_result = scan_rnf(scan_dir)

        if scan_result["files_found"]:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
                for item in scan_result["files_found"]:
                    out.write(f"[{item['risk_level']} - {item['match_reason']}] -> {item['path']}\n")
            print(f"[+] Success! Found {scan_result['total_found']} matches. Results saved to: {OUTPUT_FILE}")
        else:
            print("[-] Scan complete. No matching files or domains were found.")
