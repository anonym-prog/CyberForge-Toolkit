#!/bin/bash

# CyberForge Toolkit Installer
# Author: CyberForge Team
# Description: Automated installation script for all 30 tools

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════════╗
║       CYBERFORGE TOOLKIT INSTALLER       ║
║    30 Tools • 1 Command • Full Power     ║
╚══════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}[!] Harus dijalankan sebagai root (sudo)${NC}"
        exit 1
    fi
}

install_dependencies() {
    echo -e "${GREEN}[+] Menginstall dependencies...${NC}"
    
    # Python packages
    pip3 install --quiet --upgrade pip 2>/dev/null
    pip3 install --quiet requests BeautifulSoup4 python-nmap colorama 2>/dev/null
    
    # System packages
    if command -v apt &> /dev/null; then
        apt update -qq
        apt install -y -qq nmap hydra john curl wget netcat-openbsd dirb gobuster ffuf \
            whatweb nikto dnsutils whois bind9-host 2>/dev/null
    elif command -v pacman &> /dev/null; then
        pacman -Sy --noconfirm nmap hydra john curl wget netcat dirb gobuster ffuf \
            whatweb nikto bind whois 2>/dev/null
    fi
    
    echo -e "${GREEN}[✓] Dependencies installed${NC}"
}

setup_aliases() {
    echo -e "${GREEN}[+] Setting up aliases...${NC}"
    
    cat >> ~/.bashrc << 'EOF'

# CyberForge Toolkit Aliases
alias nmap-pro='sudo nmap -sS -sV -O -A -T4'
alias webscan='python3 ~/CyberForge-Toolkit/modules/02-scanner/webscan.py'
alias sqli='python3 ~/CyberForge-Toolkit/modules/03-exploitation/sqli_exploit.py'
alias revshell='bash ~/CyberForge-Toolkit/modules/03-exploitation/reverse_shell_gen.sh'
alias ipgeo='python3 ~/CyberForge-Toolkit/modules/01-reconnaissance/osint_harvester.py'
alias dirbuster='bash ~/CyberForge-Toolkit/modules/02-scanner/dir_buster.sh'
alias hashcrash='python3 ~/CyberForge-Toolkit/modules/07-password-cracking/hash_cracker.py'
alias cf-update='bash ~/CyberForge-Toolkit/scripts/update_all_tools.sh'
EOF
    
    source ~/.bashrc 2>/dev/null
    echo -e "${GREEN}[✓] Aliases added${NC}"
}

make_executable() {
    echo -e "${GREEN}[+] Setting executable permissions...${NC}"
    find . -name "*.sh" -exec chmod +x {} \;
    find . -name "*.py" -exec chmod +x {} \;
    chmod +x install.sh
    echo -e "${GREEN}[✓] Permissions set${NC}"
}

show_summary() {
    echo
    echo -e "${CYAN}╔══════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║        INSTALLATION COMPLETE! 🎉        ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║  30 tools siap digunakan                ║${NC}"
    echo -e "${CYAN}║  Reload terminal atau jalankan:         ║${NC}"
    echo -e "${CYAN}║  source ~/.bashrc                       ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════╝${NC}"
    echo
}

main() {
    banner
    check_root
    install_dependencies
    make_executable
    setup_aliases
    show_summary
}

main
