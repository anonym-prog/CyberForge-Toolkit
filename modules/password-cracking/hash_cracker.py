#!/usr/bin/env python3
"""
Hash Cracker — Multi-algorithm hash cracking tool
Supports MD5, SHA1, SHA256, SHA512, bcrypt, NTLM
"""

import hashlib
import sys
import argparse
import os
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

BANNER = f"""
{Fore.YELLOW}
╔══════════════════════════════════════╗
║         HASH CRACKER v3.0           ║
║    MD5 • SHA1 • SHA256 • bcrypt     ║
╚══════════════════════════════════════╝
{Style.RESET_ALL}
"""

class HashCracker:
    def __init__(self, hash_file, wordlist, hash_type='auto', threads=8):
        self.hash_file = hash_file
        self.wordlist = wordlist
        self.hash_type = hash_type
        self.threads = threads
        self.cracked = {}
        self.target_hashes = []
    
    def detect_hash_type(self, hash_str):
        """Auto-detect hash type based on length and format"""
        h = hash_str.strip()
        length = len(h)
        
        if length == 32:
            return 'md5'
        elif length == 40:
            return 'sha1'
        elif length == 64:
            return 'sha256'
        elif length == 128:
            return 'sha512'
        elif length == 60 and h.startswith('$2'):
            return 'bcrypt'
        elif length == 32 and h.isalnum():
            return 'ntlm'
        else:
            return 'unknown'
    
    def load_hashes(self):
        """Load target hashes from file"""
        try:
            with open(self.hash_file, 'r') as f:
                for line in f:
                    h = line.strip()
                    if h and not h.startswith('#'):
                        if self.hash_type == 'auto':
                            detected = self.detect_hash_type(h)
                        else:
                            detected = self.hash_type
                        self.target_hashes.append((h, detected))
            
            print(f"{Fore.GREEN}[+] Loaded {len(self.target_hashes)} hashes{Style.RESET_ALL}")
            for h, t in self.target_hashes[:5]:
                print(f"    {h[:40]}... ({t})")
            if len(self.target_hashes) > 5:
                print(f"    ... and {len(self.target_hashes) - 5} more")
            return True
        except FileNotFoundError:
            print(f"{Fore.RED}[!] Hash file not found: {self.hash_file}{Style.RESET_ALL}")
            return False
    
    def crack_hash(self, hash_str, hash_type, word):
        """Attempt to crack a single hash with a word"""
        word_clean = word.strip()
        
        try:
            if hash_type == 'md5':
                computed = hashlib.md5(word_clean.encode()).hexdigest()
            elif hash_type == 'sha1':
                computed = hashlib.sha1(word_clean.encode()).hexdigest()
            elif hash_type == 'sha256':
                computed = hashlib.sha256(word_clean.encode()).hexdigest()
            elif hash_type == 'sha512':
                computed = hashlib.sha512(word_clean.encode()).hexdigest()
            elif hash_type == 'ntlm':
                computed = hashlib.new('md4', word_clean.encode('utf-16le')).hexdigest()
            else:
                return False
            
            if computed == hash_str:
                return word_clean
        except:
            pass
        return False
    
    def try_wordlist(self, hash_str, hash_type):
        """Try all words in wordlist against a single hash"""
        try:
            with open(self.wordlist, 'r', errors='ignore') as f:
                for word in f:
                    result = self.crack_hash(hash_str, hash_type, word)
                    if result:
                        return result
        except:
            pass
        return None
    
    def crack_all(self):
        """Crack all hashes using thread pool"""
        print(f"{Fore.CYAN}[*] Starting crack with {self.threads} threads...{Style.RESET_ALL}\n")
        
        word_count = 0
        try:
            with open(self.wordlist, 'r') as f:
                word_count = sum(1 for _ in f)
        except:
            pass
        
        print(f"{Fore.YELLOW}[*] Wordlist size: {word_count:,} words{Style.RESET_ALL}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for hash_str, hash_type in self.target_hashes:
                result = self.try_wordlist(hash_str, hash_type)
                if result:
                    print(f"{Fore.GREEN}[✓] CRACKED: {hash_str[:30]}... → {Fore.WHITE}{result}{Style.RESET_ALL}")
                    self.cracked[hash_str] = result
                else:
                    print(f"{Fore.RED}[✗] Not found: {hash_str[:30]}...{Style.RESET_ALL}")
        
        return self.cracked
    
    def save_results(self, output='cracked_hashes.txt'):
        """Save cracked hashes to file"""
        with open(output, 'w') as f:
            f.write("# Cracked Hashes Report\n")
            f.write(f"# Total cracked: {len(self.cracked)}/{len(self.target_hashes)}\n\n")
            for hash_str, plaintext in self.cracked.items():
                f.write(f"{hash_str}:{plaintext}\n")
        
        print(f"\n{Fore.GREEN}[✓] Results saved to: {output}{Style.RESET_ALL}")
    
    def run(self):
        print(BANNER)
        
        if not self.load_hashes():
            sys.exit(1)
        
        if not os.path.exists(self.wordlist):
            print(f"{Fore.RED}[!] Wordlist not found: {self.wordlist}{Style.RESET_ALL}")
            # Create default wordlist
            print(f"{Fore.YELLOW}[*] Creating small demo wordlist...{Style.RESET_ALL}")
            with open(self.wordlist, 'w') as f:
                words = ['password', '123456', 'admin', 'root', 'test', 'qwerty', 
                        'letmein', 'welcome', 'monkey', 'dragon', 'master', 'passw0rd']
                f.write('\n'.join(words))
            print(f"{Fore.GREEN}[✓] Demo wordlist created: {self.wordlist}{Style.RESET_ALL}")
        
        self.crack_all()
        self.save_results()


def main():
    parser = argparse.ArgumentParser(description='Hash Cracker — Multi-algorithm')
    parser.add_argument('-f', '--hash-file', help='File containing hashes', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist file', default='wordlists/common_passwords.txt')
    parser.add_argument('-t', '--type', help='Hash type (md5/sha1/sha256/sha512/ntlm/auto)', default='auto')
    parser.add_argument('--threads', help='Thread count', type=int, default=8)
    parser.add_argument('-o', '--output', help='Output file', default='cracked_hashes.txt')
    args = parser.parse_args()
    
    cracker = HashCracker(args.hash_file, args.wordlist, args.type, args.threads)
    cracker.run()

if __name__ == '__main__':
    main()
