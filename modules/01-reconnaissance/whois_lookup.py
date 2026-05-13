#!/usr/bin/env python3
"""
Whois Lookup - Domain & IP whois information
Authorized penetration testing tool
"""
import subprocess
import sys
import json

BANNER = """
╔══════════════════════════════════════╗
║         Whois Lookup v1.0            ║
║     Domain & IP Registration Info     ║
╚══════════════════════════════════════╝
"""

def whois_lookup(target):
    """Perform whois lookup using system whois command"""
    try:
        result = subprocess.run(['whois', target], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            output = result.stdout
            
            # Extract key fields
            fields = {
                'Domain Name': '',
                'Registrar': '',
                'Creation Date': '',
                'Expiry Date': '',
                'Name Server': '',
                'Registrant Name': '',
                'Registrant Organization': '',
                'Registrant Email': '',
                'Admin Email': '',
                'Tech Email': ''
            }
            
            for line in output.split('\n'):
                for field in fields:
                    if line.lower().startswith(field.lower() + ':'):
                        value = line.split(':', 1)[1].strip()
                        if fields[field]:
                            fields[field] += f", {value}"
                        else:
                            fields[field] = value
            
            print(f"\n[+] Whois Results for: {target}")
            print(f"{'='*50}")
            for field, value in fields.items():
                if value:
                    print(f"    {field:25}: {value}")
            
            return output
        else:
            print(f"[-] Whois lookup failed")
            return None
    except subprocess.TimeoutExpired:
        print("[-] Whois lookup timed out")
        return None
    except FileNotFoundError:
        print("[-] 'whois' command not found. Install: sudo apt install whois")
        return None

def main():
    print(BANNER)
    
    target = input("[?] Enter domain or IP: ") if len(sys.argv) < 2 else sys.argv[1]
    
    print(f"\n[*] Looking up whois for: {target}")
    whois_lookup(target)
    
    print(f"\n[✓] Whois lookup complete")

if __name__ == "__main__":
    main()
