# parser.py - IOC Extraction
# Uses regex patterns to scan raw feed response text.

import re

# Precise regex patterns defined in specifications
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
DOMAIN_PATTERN = re.compile(
    r"\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|ru|cn|info|xyz|biz|cc|su|co|io|top)\b",
    re.IGNORECASE
)
SHA256_PATTERN = re.compile(r"\b([a-fA-F0-9]{64})\b")

def extract_iocs(text):
    """
    Applies regex patterns against raw text lines and extracts 
    IPs, domains, and sha256 hashes.
    """
    iocs = {
        "ips": [],
        "domains": [],
        "hashes": []
    }
    
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        # Skip comment lines
        if not line or line.startswith("#") or line.startswith("//"):
            continue
            
        # 1. Matches SHA256 hashes
        hashes_found = SHA256_PATTERN.findall(line)
        if hashes_found:
            for h in hashes_found:
                iocs["hashes"].append(h.lower())
            continue  # Avoid matching file hashes as domain parts
            
        # 2. Matches IP Addresses
        ips_found = IP_PATTERN.findall(line)
        if ips_found:
            for ip in ips_found:
                iocs["ips"].append(ip)
            continue
            
        # 3. Matches Domain Names
        domains_found = DOMAIN_PATTERN.findall(line)
        if domains_found:
            for d in domains_found:
                iocs["domains"].append(d.lower())
                
    return iocs
