import os
import json
from datetime import datetime


def scan_computer():
    # Target extensions to search for
    target_extensions = ('.msi', '.cmd', '.ps1', '.bat')

    # We scan the User profile directory safely (e.g., C:\Users\Admin)
    # This captures Desktop, Downloads, and Documents without lagging the PC
    scan_root = os.path.expanduser("~")

    print(f"🚀 Starting security scan in: {scan_root}")
    print("Please wait, logging results...")

    results = {
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_found": 0,
        "files_found": []
    }

    # os.walk loops through every folder, subfolder, and file automatically
    for root, dirs, files in os.walk(scan_root):
        for file in files:
            # Check if the file ends with any of our target extensions
            if file.lower().endswith(target_extensions):
                full_path = os.path.join(root, file)
                file_extension = os.path.splitext(file)[1].lower()

                # Append file details to our results list
                results["files_found"].append({
                    "name": file,
                    "path": full_path,
                    "type": file_extension
                })

    results["total_found"] = len(results["files_found"])

    # Step 3: Save the data into a clean .json file
    json_filename = "scan-results.json"
    with open(json_filename, "w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4)

    print(f"\n✅ Scan complete! Found {results['total_found']} matching files.")
    print(f"📂 Results successfully saved to: {json_filename}")


if __name__ == "__main__":
    scan_computer()
