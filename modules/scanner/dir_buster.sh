#!/bin/bash

# Directory Buster — Web directory/file enumeration
GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════╗
║         DIRECTORY BUSTER v3.0       ║
║    Web Directory & File Discovery    ║
╚══════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

usage() {
    echo "Usage: $0 -u <URL> [-w <wordlist>] [-t <threads>]"
    echo "  -u <URL>       Target URL (e.g., http://target.com)"
    echo "  -w <wordlist>  Path to wordlist (default: wordlists/dirs_common.txt)"
    echo "  -t <threads>   Threads (default: 10)"
    echo "  -e <ext>       File extensions (comma separated: php,txt,zip)"
    echo "  -h             Help"
    exit 1
}

URL=""
WORDLIST="wordlists/dirs_common.txt"
THREADS=10
EXTENSIONS=""

while getopts "u:w:t:e:h" opt; do
    case $opt in
        u) URL="$OPTARG" ;;
        w) WORDLIST="$OPTARG" ;;
        t) THREADS="$OPTARG" ;;
        e) EXTENSIONS="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[[ -z "$URL" ]] && usage

# Normalize URL
URL="${URL%/}"

banner
echo -e "${GREEN}[+] Target: ${URL}${NC}"
echo -e "${GREEN}[+] Wordlist: ${WORDLIST}${NC}"
echo -e "${GREEN}[+] Threads: ${THREADS}${NC}"
[[ -n "$EXTENSIONS" ]] && echo -e "${GREEN}[+] Extensions: ${EXTENSIONS}${NC}"
echo

# Check if tools available
USE_FFUF=false; USE_GOBUSTER=false; USE_DIRB=false
command -v ffuf &>/dev/null && USE_FFUF=true
command -v gobuster &>/dev/null && USE_GOBUSTER=true
command -v dirb &>/dev/null && USE_DIRB=true

if [[ ! -f "$WORDLIST" ]]; then
    echo -e "${RED}[!] Wordlist not found: ${WORDLIST}${NC}"
    echo -e "${YELLOW}[*] Creating default wordlist...${NC}"
    mkdir -p wordlists
    cat > "$WORDLIST" << 'EOF'
admin
login
wp-admin
wp-content
administrator
panel
backup
config
.config
.git
.env
uploads
images
css
js
api
v1
v2
test
dev
server-status
phpmyadmin
cgi-bin
includes
modules
templates
cache
tmp
logs
errors
src
vendor
node_modules
dist
build
public
private
docs
sql
database
db
index
home
about
contact
search
user
users
profile
settings
account
dashboard
webroot
shell
cmd
upload
download
api/v1
api/v2
graphql
rest
soap
xmlrpc
EOF
    echo -e "${GREEN}[✓] Default wordlist created with 65 entries${NC}"
fi

echo -e "${CYAN}[*] Starting directory enumeration...${NC}\n"

found=0

# Try ffuf first (fastest)
if $USE_FFUF; then
    echo -e "${YELLOW}[*] Using ffuf...${NC}"
    ext_filter=""
    [[ -n "$EXTENSIONS" ]] && ext_filter="-e .${EXTENSIONS//,/,.}"
    ffuf -u "${URL}/FUZZ" -w "$WORDLIST" -t "$THREADS" -c -fc 404,403 $ext_filter 2>/dev/null
    found=1
fi

# Fallback to gobuster
if ! $USE_FFUF && $USE_GOBUSTER; then
    echo -e "${YELLOW}[*] Using gobuster...${NC}"
    ext_flag=""
    [[ -n "$EXTENSIONS" ]] && ext_flag="-x $EXTENSIONS"
    gobuster dir -u "$URL" -w "$WORDLIST" -t "$THREADS" -q $ext_flag 2>/dev/null
    found=1
fi

# Fallback to dirb
if ! $USE_FFUF && ! $USE_GOBUSTER && $USE_DIRB; then
    echo -e "${YELLOW}[*] Using dirb...${NC}"
    ext_flag=""
    [[ -n "$EXTENSIONS" ]] && ext_flag="-X .${EXTENSIONS//,/,.}"
    dirb "$URL" "$WORDLIST" $ext_flag -r -S 2>/dev/null | grep "+ "
    found=1
fi

# Manual curl-based scanner (no tools)
if [[ $found -eq 0 ]]; then
    echo -e "${YELLOW}[*] No scanner tools found. Using curl (slow)...${NC}"
    echo -e "${YELLOW}[*] This will take a while...${NC}\n"
    
    while IFS= read -r dir; do
        [[ -z "$dir" ]] && continue
        
        url="${URL}/${dir}"
        resp=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 5 "$url" 2>/dev/null)
        
        if [[ "$resp" != "404" && "$resp" != "000" ]]; then
            echo -e "${GREEN}[${resp}] ${url}${NC}"
        fi
        
        # Also check with extensions
        if [[ -n "$EXTENSIONS" ]]; then
            IFS=',' read -ra EXTS <<< "$EXTENSIONS"
            for ext in "${EXTS[@]}"; do
                url_ext="${URL}/${dir}.${ext}"
                resp_ext=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 --max-time 5 "$url_ext" 2>/dev/null)
                if [[ "$resp_ext" != "404" && "$resp_ext" != "000" ]]; then
                    echo -e "${GREEN}[${resp_ext}] ${url_ext}${NC}"
                fi
            done
        fi
    done < "$WORDLIST"
fi

echo -e "\n${GREEN}[✓] Directory enumeration complete${NC}"
