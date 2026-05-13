#!/bin/bash

# ==============================================================
# CyberForge Toolkit Aliases
# Load dengan: source config/aliases.sh
# ==============================================================

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════╗"
echo "║     CyberForge Aliases Loaded! 🚀        ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${NC}"

# ---- RECONNAISSANCE ----
alias nmap-pro='sudo nmap -sS -sV -O -A -T4 -p-'
alias nmap-quick='sudo nmap -sS -sV -T4 --top-ports 1000'
alias nmap-stealth='sudo nmap -sS -sV -T2 -f -D RND:10'
alias subenum='bash modules/01-reconnaissance/subdomain_enum.sh'
alias dnsrecon='bash modules/01-reconnaissance/dns_recon.sh'
alias osint='python3 modules/01-reconnaissance/osint_harvester.py'
alias ipgeo='python3 modules/01-reconnaissance/osint_harvester.py -t'

# ---- SCANNER ----
alias webscan='python3 modules/02-scanner/webscan.py'
alias vulnscan='bash modules/02-scanner/vuln_scanner.sh'
alias portscan='python3 modules/02-scanner/port_scanner.py'
alias dirbust='bash modules/02-scanner/dir_buster.sh'
alias cmsscan='bash modules/02-scanner/cms_scanner.sh'

# ---- EXPLOITATION ----
alias sqli='python3 modules/03-exploitation/sqli_exploit.py'
alias xsspay='python3 modules/03-exploitation/xss_payloader.py'
alias revshell='bash modules/03-exploitation/reverse_shell_gen.sh'
alias msfwrap='bash modules/03-exploitation/metasploit_wrapper.sh'
alias lfirfi='bash modules/03-exploitation/lfi_rfi_checker.sh'

# ---- POST-EXPLOITATION ----
alias privesc='bash modules/04-post-exploitation/privilege_esc.sh'
alias credharvest='bash modules/04-post-exploitation/cred_harvester.sh'
alias persist='python3 modules/04-post-exploitation/persistence.py'

# ---- WEB APPLICATION ----
alias jwthack='python3 modules/05-web-application/jwt_toolkit.py'
alias apifuzz='python3 modules/05-web-application/api_fuzzer.py'
alias csrfpoc='bash modules/05-web-application/csrf_poc_gen.sh'
alias ssrfcheck='bash modules/05-web-application/ssrf_checker.sh'
alias uploadbypass='bash modules/05-web-application/file_upload_bypass.sh'

# ---- WIRELESS ----
alias wifiaudit='bash modules/06-wireless/wifi_audit.sh'
alias blescan='bash modules/06-wireless/bluetooth_le.sh'

# ---- PASSWORD ----
alias hashcrash='python3 modules/07-password-cracking/hash_cracker.py'
alias bruteforce='bash modules/07-password-cracking/brute_force.sh'

# ---- FORENSICS ----
alias memanalyze='python3 modules/08-forensics/memory_analyzer.py'
alias diskforensic='bash modules/08-forensics/disk_forensics.sh'

# ---- REVERSE ENGINEERING ----
alias binanalyze='python3 modules/09-reverse-engineering/binary_analysis.py'

# ---- UTILITY ----
alias cf-update='bash scripts/update_all_tools.sh'
alias cf-setup='sudo bash install.sh'
alias cf-banner='cat banner.txt'

echo -e "${GREEN}✓ 30 tool aliases siap digunakan!${NC}"
echo -e "${CYAN}Ketik nama alias untuk menjalankan tool (e.g., 'webscan -u http://target.com')${NC}"
