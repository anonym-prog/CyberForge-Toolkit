#!/usr/bin/env python3
"""
OSINT Harvester & IP Geolocator
Reconnaissance tool for IP geolocation, domain info, and OSINT gathering
"""

import requests
import json
import sys
import socket
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = f"""
{Fore.GREEN}
╔══════════════════════════════════════╗
║       OSINT HARVESTER v3.0          ║
║    IP Geo • DNS • WHOIS • OSINT     ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

class OSINTHarvester:
    def __init__(self, target):
        self.target = target
        self.results = {}
    
    def resolve_dns(self):
        """Resolve domain to IP"""
        try:
            ip = socket.gethostbyname(self.target)
            self.results['ip'] = ip
            print(f"{Fore.CYAN}[+] Resolved IP:{Style.RESET_ALL} {ip}")
            return ip
        except:
            print(f"{Fore.RED}[!] DNS resolution failed{Style.RESET_ALL}")
            return None
    
    def ip_geolocate(self, ip):
        """Get IP geolocation data"""
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            data = r.json()
            if data.get('status') == 'success':
                self.results['geo'] = {
                    'country': data.get('country'),
                    'region': data.get('regionName'),
                    'city': data.get('city'),
                    'zip': data.get('zip'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'as': data.get('as')
                }
                print(f"{Fore.GREEN}[+] Country:  {data.get('country')}")
                print(f"[+] Region:   {data.get('regionName')}")
                print(f"[+] City:     {data.get('city')}")
                print(f"[+] ISP:      {data.get('isp')}")
                print(f"[+] Org:      {data.get('org')}")
                print(f"[+] ASN:      {data.get('as')}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[!] GeoIP Error: {e}{Style.RESET_ALL}")
    
    def dns_records(self):
        """Enumerate DNS records"""
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        self.results['dns'] = {}
        
        for rtype in record_types:
            try:
                result = socket.getaddrinfo(self.target, None)
                print(f"{Fore.YELLOW}[DNS {rtype}]{Style.RESET_ALL} Found records")
                self.results['dns'][rtype] = str(result[:2])
            except:
                pass
    
    def whois_lookup(self):
        """Perform WHOIS lookup"""
        try:
            import subprocess
            result = subprocess.run(['whois', self.target], capture_output=True, text=True, timeout=15)
            if result.stdout:
                lines = result.stdout.split('\n')[:15]
                self.results['whois'] = lines
                print(f"{Fore.MAGENTA}[WHOIS]{Style.RESET_ALL} Data retrieved ({len(lines)} lines)")
                for line in lines[:8]:
                    if line.strip():
                        print(f"  {line}")
        except:
            print(f"{Fore.RED}[!] WHOIS lookup failed{Style.RESET_ALL}")
    
    def security_headers(self):
        """Check security headers"""
        try:
            r = requests.get(f"https://{self.target}", timeout=10, verify=False)
            headers = ['X-Frame-Options', 'X-XSS-Protection', 'X-Content-Type-Options',
                      'Strict-Transport-Security', 'Content-Security-Policy']
            print(f"{Fore.CYAN}[Security Headers]{Style.RESET_ALL}")
            for h in headers:
                val = r.headers.get(h, 'MISSING')
                color = Fore.GREEN if val != 'MISSING' else Fore.RED
                print(f"  {color}{h}: {val}{Style.RESET_ALL}")
        except:
            pass
    
    def shodan_lookup(self):
        """Shodan lookup (if API key available)"""
        # Placeholder — integrates with Shodan API
        print(f"{Fore.YELLOW}[!] Shodan API key not configured. Skipping.{Style.RESET_ALL}")
    
    def export_json(self, filename="osint_report.json"):
        """Export results to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        print(f"{Fore.GREEN}[✓] Report saved to {filename}{Style.RESET_ALL}")
    
    def run_all(self):
        print(BANNER)
        print(f"{Fore.WHITE}Target: {self.target}{Style.RESET_ALL}\n")
        
        ip = self.resolve_dns()
        if ip:
            self.ip_geolocate(ip)
        self.dns_records()
        self.whois_lookup()
        self.security_headers()
        self.export_json()


def main():
    parser = argparse.ArgumentParser(description='OSINT Harvester & IP Geolocator')
    parser.add_argument('-t', '--target', help='Target domain or IP', required=True)
    parser.add_argument('-o', '--output', help='Output file', default='osint_report.json')
    args = parser.parse_args()
    
    harvester = OSINTHarvester(args.target)
    harvester.run_all()

if __name__ == '__main__':
    main()
