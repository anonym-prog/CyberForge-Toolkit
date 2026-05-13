#!/usr/bin/env python3
"""
DNS Recon - Comprehensive DNS enumeration
Authorized penetration testing tool
"""
import sys
import socket
import dns.resolver
import dns.zone
import dns.query

BANNER = """
╔══════════════════════════════════════╗
║          DNS Recon v1.0              ║
║     DNS Enumeration & Zone Transfer   ║
╚══════════════════════════════════════╝
"""

def get_nameservers(domain):
    """Get nameservers for domain"""
    try:
        answers = dns.resolver.resolve(domain, 'NS')
        ns_list = [str(rdata) for rdata in answers]
        print(f"[+] Nameservers: {', '.join(ns_list)}")
        return ns_list
    except:
        print("[-] No NS records found")
        return []

def try_zone_transfer(domain, ns):
    """Attempt DNS zone transfer"""
    try:
        ns_ip = socket.gethostbyname(ns)
        zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain, timeout=10))
        print(f"\n[!] ZONE TRANSFER SUCCESSFUL on {ns}!")
        print(f"[!] Retrieved {len(zone.nodes)} records")
        for name, node in zone.nodes.items():
            rdatasets = node.rdatasets
            for rdataset in rdatasets:
                print(f"    {str(name):30} {rdataset}")
        return True
    except Exception as e:
        print(f"[-] Zone transfer failed on {ns}: {e}")
        return False

def enumerate_records(domain):
    """Enumerate common DNS records"""
    record_types = {
        'A': 'IPv4 Address',
        'AAAA': 'IPv6 Address', 
        'MX': 'Mail Exchange',
        'CNAME': 'Canonical Name',
        'TXT': 'Text Record',
        'SOA': 'Start of Authority',
        'SRV': 'Service Record',
        'CAA': 'Certification Authority'
    }
    
    for rtype, desc in record_types.items():
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for rdata in answers:
                print(f"    {rtype:6} ({desc:20}) : {rdata}")
        except:
            pass

def main():
    print(BANNER)
    
    domain = input("[?] Enter domain: ") if len(sys.argv) < 2 else sys.argv[1]
    
    print(f"\n[*] Starting DNS recon for: {domain}\n")
    
    # Basic resolution
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] Resolved to: {ip}")
    except:
        print(f"[-] Cannot resolve {domain}")
        return
    
    # Enumerate records
    print(f"\n[+] DNS Records:")
    enumerate_records(domain)
    
    # Get nameservers
    print(f"\n[+] Nameserver Discovery:")
    ns_list = get_nameservers(domain)
    
    # Try zone transfer
    if ns_list:
        print(f"\n[+] Attempting Zone Transfer:")
        for ns in ns_list:
            ns = ns.rstrip('.')
            try_zone_transfer(domain, ns)
    
    print(f"\n[✓] DNS recon complete for {domain}")

if __name__ == "__main__":
    main()
