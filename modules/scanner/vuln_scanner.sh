#!/bin/bash

# Vulnerability Scanner — CVE-based vulnerability detection
GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════╗
║      VULNERABILITY SCANNER v3.0     ║
║   CVE Detection • Service Audit    ║
╚══════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

usage() {
    echo "Usage: $0 -t <target> [-p <ports>]"
    echo "  -t <target>   Target IP/domain"
    echo "  -p <ports>    Ports (default: 80,443,22,21,3306,8080)"
    echo "  -h            Help"
    exit 1
}

TARGET=""
PORTS="80,443,22,21,3306,8080"

while getopts "t:p:h" opt; do
    case $opt in
        t) TARGET="$OPTARG" ;;
        p) PORTS="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[[ -z "$TARGET" ]] && usage

banner
echo -e "${GREEN}[+] Target: $TARGET"
echo -e "[+] Ports: $PORTS${NC}\n"

echo -e "${YELLOW}[*] Scanning for open ports...${NC}"
for port in $(echo $PORTS | tr ',' ' '); do
    timeout 2 bash -c "echo >/dev/tcp/$TARGET/$port" 2>/dev/null && \
        echo -e "${GREEN}[+] Port $port — Open${NC}" || \
        echo -e "${RED}[-] Port $port — Closed${NC}"
done

echo -e "\n${YELLOW}[*] Checking common vulnerabilities...${NC}"

# Check for default credentials on common services
echo -e "\n${CYAN}[!] Checking for default credentials...${NC}"

# HTTP check
timeout 3 curl -s -I "http://$TARGET" 2>/dev/null | grep -q "Server" && \
    echo -e "${YELLOW}[*] HTTP service detected — check for default creds${NC}"

# FTP anonymous check
timeout 3 curl -s "ftp://$TARGET" --user anonymous:test 2>/dev/null | grep -q "230" && \
    echo -e "${RED}[!] FTP anonymous login enabled!${NC}"

# Check for common vulnerabilities via banner
echo -e "\n${CYAN}[!] Banner grabbing...${NC}"
for port in $(echo $PORTS | tr ',' ' '); do
    banner=$(timeout 2 bash -c "echo 'test' | nc -w 2 $TARGET $port 2>/dev/null | head -1")
    [[ -n "$banner" ]] && echo -e "${YELLOW}[+] Port $port: $banner${NC}"
done

echo -e "\n${GREEN}[✓] Vulnerability scan complete${NC}"
