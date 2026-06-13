# validator.py - Validation & Deduplication
# Deduplicates listings and filters out private RFC1918 networks.

def is_valid_public_ip(ip):
    """
    Returns True if an IP is a valid public IPv4 address,
    excluding RFC1918 private ranges and loopback.
    """
    try:
        parts = [int(p) for p in ip.split(".")]
        if len(parts) != 4:
            return False
            
        # Check standard byte ranges
        if any(p < 0 or p > 255 for p in parts):
            return False
            
        # Loopback
        if parts[0] == 127:
            return False
            
        # RFC1918 Private ranges:
        # 10.0.0.0/8
        if parts[0] == 10:
            return False
        # 172.16.0.0/12
        if parts[0] == 172 and (16 <= parts[1] <= 31):
            return False
        # 192.168.0.0/16
        if parts[0] == 192 and parts[1] == 168:
            return False
            
        return True
    except (ValueError, IndexError):
        return False

def validate_iocs(ioc_dict):
    """
    Validates and deduplicates the indicators of compromise.
    Converts list values to sorted deduplicated collections.
    """
    validated = {
        "ips": [],
        "domains": [],
        "hashes": []
    }
    
    # Deduplicate and validate IPs
    raw_ips = ioc_dict.get("ips", [])
    unique_ips = set(raw_ips)
    valid_ips = [ip for ip in unique_ips if is_valid_public_ip(ip)]
    validated["ips"] = sorted(valid_ips)
    
    # Deduplicate domains (and exclude obvious false positives)
    raw_domains = ioc_dict.get("domains", [])
    valid_domains = [d for d in set(raw_domains) if d != "localhost"]
    validated["domains"] = sorted(valid_domains)
    
    # Deduplicate hashes
    raw_hashes = ioc_dict.get("hashes", [])
    validated["hashes"] = sorted(list(set(raw_hashes)))
    
    return validated
