#!/usr/bin/env python3
"""
Memory Analyzer — RAM dump analysis using Volatility
Process listing, network connections, registry, and more
"""

import subprocess
import sys
import os
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

BANNER = f"""
{Fore.BLUE}
╔══════════════════════════════════════╗
║       MEMORY ANALYZER v3.0          ║
║   RAM Forensics • Process Dump     ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

class MemoryAnalyzer:
    def __init__(self, dump_file, profile=None):
        self.dump_file = dump_file
        self.profile = profile
        self.vol_path = self.find_volatility()
    
    def find_volatility(self):
        """Find volatility3 or volatility2"""
        for cmd in ['volatility3', 'vol', 'volatility']:
            result = subprocess.run(['which', cmd], capture_output=True, text=True)
            if result.stdout.strip():
                return result.stdout.strip()
        
        # Check common paths
        for path in ['/usr/bin/volatility3', '/usr/local/bin/volatility3',
                     '/opt/volatility3/vol.py', '~/tools/volatility3/vol.py']:
            path = os.path.expanduser(path)
            if os.path.exists(path):
                return path
        
        return None
    
    def is_vol3(self):
        """Check if using Volatility 3"""
        return 'volatility3' in (self.vol_path or '') or 'vol.py' in (self.vol_path or '')
    
    def run_command(self, plugin, args=None):
        """Run a volatility command"""
        if not self.vol_path:
            print(f"{Fore.RED}[!] Volatility not found. Install with: pip install volatility3{Style.RESET_ALL}")
            return None
        
        cmd = []
        if self.is_vol3():
            cmd = ['python3', self.vol_path, '-f', self.dump_file]
            if self.profile:
                cmd.extend(['--profile', self.profile])
            cmd.append(plugin)
        else:
            cmd = [self.vol_path, '-f', self.dump_file]
            if self.profile:
                cmd.extend(['--profile', self.profile])
            cmd.append(plugin)
        
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return result.stdout
        except subprocess.TimeoutExpired:
            return f"{Fore.RED}[!] Command timed out{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}"
    
    def detect_profile(self):
        """Auto-detect memory profile"""
        print(f"{Fore.YELLOW}[*] Detecting memory profile...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('banners.Banners')
        else:
            output = self.run_command('imageinfo')
        
        if output:
            print(output[:500])
            # Try to extract profile
            if 'Suggested Profile(s)' in output:
                import re
                profiles = re.findall(r'(\w+Win\w+SP\d)', output)
                if profiles:
                    self.profile = profiles[0]
                    print(f"{Fore.GREEN}[+] Auto-detected profile: {self.profile}{Style.RESET_ALL}")
        
        return self.profile
    
    def list_processes(self):
        """List running processes"""
        print(f"\n{Fore.CYAN}[*] Listing processes...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('windows.pslist')
        else:
            output = self.run_command('pslist')
        
        if output:
            print(output[:2000])
        return output
    
    def network_connections(self):
        """List network connections"""
        print(f"\n{Fore.CYAN}[*] Network connections...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('windows.netscan')
        else:
            output = self.run_command('netscan')
        
        if output:
            print(output[:2000])
        return output
    
    def dump_process(self, pid):
        """Dump a specific process"""
        print(f"\n{Fore.CYAN}[*] Dumping process {pid}...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('windows.dumpfiles.DumpFiles', 
                                       ['--pid', str(pid), '--dump'])
        else:
            output = self.run_command('procdump', ['-p', str(pid), '-D', 'dumps/'])
        
        if output:
            print(output[:500])
        return output
    
    def cmdline(self):
        """Extract command line history"""
        print(f"\n{Fore.CYAN}[*] Command line history...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('windows.cmdline')
        else:
            output = self.run_command('cmdline')
        
        if output:
            print(output[:2000])
        return output
    
    def registry_hives(self):
        """List registry hives"""
        print(f"\n{Fore.CYAN}[*] Registry hives...{Style.RESET_ALL}")
        
        if self.is_vol3():
            output = self.run_command('windows.registry.hivelist')
        else:
            output = self.run_command('hivelist')
        
        if output:
            print(output[:1000])
        return output
    
    def run_all(self):
        """Run all memory analysis"""
        print(BANNER)
        print(f"{Fore.WHITE}Memory dump: {self.dump_file}{Style.RESET_ALL}\n")
        
        if not self.vol_path:
            print(f"{Fore.RED}[!] Volatility not installed. Install with:{Style.RESET_ALL}")
            print("  pip install volatility3")
            print("  or: sudo apt install volatility")
            return
        
        if not self.profile:
            self.detect_profile()
        
        self.list_processes()
        self.network_connections()
        self.cmdline()
        
        print(f"\n{Fore.GREEN}[✓] Analysis complete{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(description='Memory Analyzer — RAM Forensics')
    parser.add_argument('-f', '--file', help='Memory dump file (.raw/.mem/.dmp)', required=True)
    parser.add_argument('--profile', help='Memory profile (e.g., Win10x64_19041)')
    parser.add_argument('--pslist', action='store_true', help='List processes')
    parser.add_argument('--netscan', action='store_true', help='Network connections')
    parser.add_argument('--cmdline', action='store_true', help='Command line history')
    parser.add_argument('--dump-pid', type=int, help='Dump specific PID')
    parser.add_argument('--all', action='store_true', help='Run all analysis')
    args = parser.parse_args()
    
    analyzer = MemoryAnalyzer(args.file, args.profile)
    
    if args.all or not any([args.pslist, args.netscan, args.cmdline, args.dump_pid]):
        analyzer.run_all()
    else:
        if args.pslist:
            analyzer.list_processes()
        if args.netscan:
            analyzer.network_connections()
        if args.cmdline:
            analyzer.cmdline()
        if args.dump_pid:
            analyzer.dump_process(args.dump_pid)


if __name__ == '__main__':
    main()
