import os
import platform

def load_domains(domain_file):
    """Loads a list of domains from the specified text file."""
    if not os.path.exists(domain_file):
        print(f"[-] Error: Could not find domain file: {domain_file}")
        return []
    
    with open(domain_file, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file.readlines() if line.strip()]

def get_scan_directory():
    """Detects the OS and returns the safest, most comprehensive user directory to scan."""
    current_os = platform.system().lower()
    home_dir = os.path.expanduser('~')
    
    print(f"[*] Detected Operating System: {platform.system()} ({platform.processor()})")
    return home_dir

def scan_system(start_path, domains, output_file):
    """Scans the directory for .msi files or files matching domain names."""
    print(f"[*] Starting scan in user directory: {start_path}")
    print(f"[*] Checking for '.msi' extensions and {len(domains)} target domains...")
    
    found_items = []
    
    # os.walk automatically handles forward slashes (Mac) and backslashes (Windows)
    for root, dirs, files in os.walk(start_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            filename_lower = filename.lower()
            
            # Condition 1: Check if the file is a Windows Installer (.msi)
            if filename_lower.endswith('.msi'):
                found_items.append(f"[MSI FILE FOUND] -> {file_path}")
                continue
            
            # Condition 2: Check if any domain from RNF.txt is inside the filename
            for domain in domains:
                if domain in filename_lower:
                    found_items.append(f"[DOMAIN MATCH - {domain}] -> {file_path}")
                    break  # Stop checking other domains for this file once matched
                    
    # Write the results to the output log
    if found_items:
        with open(output_file, 'w', encoding='utf-8') as out:
            for item in found_items:
                out.write(item + "\n")
        print(f"[+] Success! Found {len(found_items)} matches. Results saved to: {output_file}")
    else:
        print("[-] Scan complete. No matching files or domains were found.")

if __name__ == "__main__":
    # Configuration
    DOMAIN_LIST_FILE = "RNF.txt"
    OUTPUT_FILE = "scan_results.txt"
    
    # Run the configuration and scanner
    target_domains = load_domains(DOMAIN_LIST_FILE)
    
    if target_domains:
        scan_dir = get_scan_directory()
        scan_system(scan_dir, target_domains, OUTPUT_FILE)
