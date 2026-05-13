#!/usr/bin/env python3
"""
Web Vulnerability Scanner — Multi-Engine Scanner
Detects SQLi, XSS, LFI, RFI, Open Redirect, and more
"""

import requests
import sys
import argparse
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}
╔══════════════════════════════════════╗
║         WEBSCAN v3.0                ║
║  Multi-Engine Vulnerability Scanner  ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

class WebVulnScanner:
    def __init__(self, url, threads=5):
        self.url = url
        self.threads = threads
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'CyberForge-Scanner/3.0',
            'Accept': 'text/html,application/xhtml+xml'
        })
        self.vulnerabilities = []
    
    def check_live(self):
        """Check if target is alive"""
        try:
            r = self.session.get(self.url, timeout=10)
            print(f"{Fore.GREEN}[+] Target live: {r.status_code}{Style.RESET_ALL}")
            return True
        except:
            print(f"{Fore.RED}[!] Target unreachable{Style.RESET_ALL}")
            return False
    
    def check_sqli(self):
        """Basic SQL Injection detection"""
        print(f"{Fore.YELLOW}[*] Testing SQL Injection...{Style.RESET_ALL}")
        payloads = ["'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1", "' OR 1=1--", "' UNION SELECT 1--"]
        errors = ["SQL syntax", "MySQL", "ORA-", "syntax error", "Unclosed quotation mark"]
        
        for payload in payloads:
            try:
                r = self.session.get(f"{self.url}?id={payload}", timeout=10)
                for error in errors:
                    if error.lower() in r.text.lower():
                        print(f"{Fore.RED}[!] SQLi detected with payload: {payload}{Style.RESET_ALL}")
                        self.vulnerabilities.append(f"SQLi: {payload}")
                        return True
            except:
                pass
        print(f"{Fore.GREEN}[-] No obvious SQLi detected{Style.RESET_ALL}")
        return False
    
    def check_xss(self):
        """Cross-Site Scripting detection"""
        print(f"{Fore.YELLOW}[*] Testing XSS...{Style.RESET_ALL}")
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>"
        ]
        
        for payload in payloads:
            try:
                r = self.session.get(f"{self.url}?q={payload}", timeout=10)
                if payload in r.text:
                    print(f"{Fore.RED}[!] XSS detected!{Style.RESET_ALL}")
                    self.vulnerabilities.append(f"XSS: {payload[:30]}")
                    return True
            except:
                pass
        print(f"{Fore.GREEN}[-] No obvious XSS detected{Style.RESET_ALL}")
        return False
    
    def check_lfi(self):
        """Local File Inclusion detection"""
        print(f"{Fore.YELLOW}[*] Testing LFI...{Style.RESET_ALL}")
        payloads = [
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "....//....//....//etc/passwd",
            "/etc/passwd",
            "..\\..\\..\\windows\\win.ini"
        ]
        
        for payload in payloads:
            try:
                r = self.session.get(f"{self.url}?file={payload}", timeout=10)
                if "root:" in r.text or "[extensions]" in r.text:
                    print(f"{Fore.RED}[!] LFI detected!{Style.RESET_ALL}")
                    self.vulnerabilities.append(f"LFI: {payload}")
                    return True
            except:
                pass
        print(f"{Fore.GREEN}[-] No obvious LFI detected{Style.RESET_ALL}")
        return False
    
    def check_open_redirect(self):
        """Open Redirect detection"""
        print(f"{Fore.YELLOW}[*] Testing Open Redirect...{Style.RESET_ALL}")
        test_url = "https://evil.com"
        payloads = [f"//evil.com", f"https://evil.com", f"////evil.com"]
        
        for payload in payloads:
            try:
                r = self.session.get(f"{self.url}?next={payload}", timeout=10, allow_redirects=False)
                if r.status_code in [301, 302]:
                    location = r.headers.get('Location', '')
                    if 'evil.com' in location:
                        print(f"{Fore.RED}[!] Open Redirect detected!{Style.RESET_ALL}")
                        self.vulnerabilities.append(f"Open Redirect: {payload}")
                        return True
            except:
                pass
        print(f"{Fore.GREEN}[-] No open redirect detected{Style.RESET_ALL}")
        return False
    
    def check_headers(self):
        """Check security headers"""
        print(f"{Fore.YELLOW}[*] Checking security headers...{Style.RESET_ALL}")
        try:
            r = self.session.get(self.url, timeout=10)
            checks = {
                'X-Frame-Options': ['DENY', 'SAMEORIGIN'],
                'X-Content-Type-Options': ['nosniff'],
                'Strict-Transport-Security': ['max-age='],
                'Content-Security-Policy': ["default-src"],
                'X-XSS-Protection': ['1']
            }
            
            for header, expected in checks.items():
                value = r.headers.get(header, '')
                if not value or not any(e in value for e in expected):
                    print(f"{Fore.RED}[!] Missing/insecure: {header}{Style.RESET_ALL}")
                    self.vulnerabilities.append(f"Missing header: {header}")
                else:
                    print(f"{Fore.GREEN}[✓] {header}: {value[:50]}{Style.RESET_ALL}")
        except:
            pass
    
    def server_info(self):
        """Gather server information"""
        print(f"{Fore.YELLOW}[*] Gathering server info...{Style.RESET_ALL}")
        try:
            r = self.session.get(self.url, timeout=10)
            server = r.headers.get('Server', 'Unknown')
            powered = r.headers.get('X-Powered-By', 'Unknown')
            print(f"{Fore.CYAN}[+] Server: {server}")
            print(f"[+] Powered by: {powered}")
            print(f"[+] Content-Type: {r.headers.get('Content-Type', 'Unknown')}{Style.RESET_ALL}")
        except:
            pass
    
    def generate_report(self):
        """Generate vulnerability report"""
        print(f"\n{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║           SCAN COMPLETE              ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
        
        if self.vulnerabilities:
            print(f"\n{Fore.RED}[!] Vulnerabilities found: {len(self.vulnerabilities)}{Style.RESET_ALL}")
            for v in self.vulnerabilities:
                print(f"  {Fore.RED}• {v}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}[✓] No obvious vulnerabilities detected{Style.RESET_ALL}")
        
        # Save report
        with open("webscan_report.txt", "w") as f:
            f.write(f"WebScan Report for {self.url}\n")
            f.write(f"{'='*40}\n")
            for v in self.vulnerabilities:
                f.write(f"- {v}\n")
        print(f"{Fore.GREEN}[✓] Report saved to webscan_report.txt{Style.RESET_ALL}")
    
    def run(self):
        print(BANNER)
        print(f"{Fore.WHITE}Target: {self.url}{Style.RESET_ALL}\n")
        
        if not self.check_live():
            sys.exit(1)
        
        self.server_info()
        self.check_headers()
        self.check_sqli()
        self.check_xss()
        self.check_lfi()
        self.check_open_redirect()
        self.generate_report()


def main():
    parser = argparse.ArgumentParser(description='Web Vulnerability Scanner')
    parser.add_argument('-u', '--url', help='Target URL', required=True)
    parser.add_argument('-t', '--threads', help='Threads', type=int, default=5)
    args = parser.parse_args()
    
    scanner = WebVulnScanner(args.url, args.threads)
    scanner.run()

if __name__ == '__main__':
    main()
