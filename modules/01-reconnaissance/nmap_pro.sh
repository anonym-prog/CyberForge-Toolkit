#!/bin/bash

# Nmap Pro - Advanced Nmap scanning toolkit
# Authorized penetration testing tool

BANNER='''
╔══════════════════════════════════════╗
║          Nmap Pro v1.0               ║
║     Advanced Network Scanning         ║
╚══════════════════════════════════════╝
'''

echo "$BANNER"

if [ -z "$1" ]; then
    echo "Usage: $0 <target> [scan_type]"
    echo ""
    echo "Scan Types:"
    echo "  1  - Quick scan (top 100 ports)"
    echo "  2  - Full scan (1-65535 ports)"
    echo "  3  - Service/Version detection"
    echo "  4  - OS detection"
    echo "  5  - Aggressive scan"
    echo "  6  - UDP scan"
    echo "  7  - Ping sweep (subnet /24)"
    echo "  8  - Vulnerability scan (NSE vuln)"
    echo "  9  - Full NSE scan"
    echo "  10 - Custom arguments"
    echo ""
    read -p "Select scan type [1-10]: " SCAN_TYPE
else
    SCAN_TYPE="${2:-1}"
fi

TARGET="$1"
OUTPUT="output/nmap_${TARGET}_$(date +%Y%m%d_%H%M%S)"
mkdir -p output 2>/dev/null

case $SCAN_TYPE in
    1)
        echo "[*] Running quick scan on $TARGET..."
        nmap -T4 -F -oN "${OUTPUT}_quick.txt" "$TARGET"
        ;;
    2)
        echo "[*] Running full port scan on $TARGET..."
        nmap -T4 -p- -oN "${OUTPUT}_full.txt" "$TARGET"
        ;;
    3)
        echo "[*] Running service detection on $TARGET..."
        nmap -T4 -sV -oN "${OUTPUT}_service.txt" "$TARGET"
        ;;
    4)
        echo "[*] Running OS detection on $TARGET..."
        nmap -T4 -O -oN "${OUTPUT}_os.txt" "$TARGET"
        ;;
    5)
        echo "[*] Running aggressive scan on $TARGET..."
        nmap -T4 -A -oN "${OUTPUT}_aggressive.txt" "$TARGET"
        ;;
    6)
        echo "[*] Running UDP scan on $TARGET..."
        nmap -T4 -sU --top-ports 100 -oN "${OUTPUT}_udp.txt" "$TARGET"
        ;;
    7)
        echo "[*] Running ping sweep on $TARGET/24..."
        nmap -T4 -sn "$TARGET/24" -oN "${OUTPUT}_pingsweep.txt"
        ;;
    8)
        echo "[*] Running vulnerability scan on $TARGET..."
        nmap -T4 --script vuln -oN "${OUTPUT}_vuln.txt" "$TARGET"
        ;;
    9)
        echo "[*] Running full NSE scan on $TARGET..."
        nmap -T4 --script "default or safe or vuln" -oN "${OUTPUT}_nse.txt" "$TARGET"
        ;;
    10)
        read -p "Enter custom nmap arguments: " CUSTOM_ARGS
        echo "[*] Running: nmap $CUSTOM_ARGS $TARGET"
        nmap $CUSTOM_ARGS "$TARGET" -oN "${OUTPUT}_custom.txt"
        ;;
    *)
        echo "[-] Invalid option"
        exit 1
        ;;
esac

echo ""
echo "[✓] Scan complete. Results saved to output/"
