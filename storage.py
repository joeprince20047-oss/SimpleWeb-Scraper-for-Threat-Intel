# storage.py - Serialization / Output Layer
# Serializes indicators to JSON, CSV, or plain TXT files.

import os
import json
import csv
from datetime import datetime

def save_json(iocs, feed_name, filepath):
    """Writes pretty-printed JSON representation with timestamp metadata"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    data = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "feed": feed_name,
        "counts": {
            "ips": len(iocs["ips"]),
            "domains": len(iocs["domains"]),
            "hashes": len(iocs["hashes"])
        },
        "iocs": iocs
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[*] Successfully saved {sum(data['counts'].values())} IOCs to: {filepath}")

def save_csv(iocs, filepath):
    """Writes flat spreadsheet row entries of format [Type, Value]"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Value"])
        
        for ip in iocs["ips"]:
            writer.writerow(["IP Address", ip])
        for domain in iocs["domains"]:
            writer.writerow(["Domain Name", domain])
        for h in iocs["hashes"]:
            writer.writerow(["SHA256 Hash", h])
            
    total_rows = len(iocs["ips"]) + len(iocs["domains"]) + len(iocs["hashes"])
    print(f"[*] Successfully saved {total_rows} entries to: {filepath}")

def save_txt(iocs, filepath):
    """Writes one line text entries grouped together with section headers"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        if iocs["ips"]:
            f.write("=== IP ADDRESSES ===\n")
            for ip in iocs["ips"]:
                f.write(f"{ip}\n")
            f.write("\n")
            
        if iocs["domains"]:
            f.write("=== DOMAIN NAMES ===\n")
            for domain in iocs["domains"]:
                f.write(f"{domain}\n")
            f.write("\n")
            
        if iocs["hashes"]:
            f.write("=== FILE HASHES ===\n")
            for h in iocs["hashes"]:
                f.write(f"{h}\n")
            f.write("\n")
            
    print(f"[*] Successfully saved sorted lists to format TXT: {filepath}")
