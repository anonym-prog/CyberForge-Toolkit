#!/bin/bash

# Subdomain Enumerator — DNS brute force + API-based enumeration
GREEN='\033[0;32m'; RED='\033[0;31m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔══════════════════════════════════════╗
║     SUBDOMAIN ENUMERATOR v3.0       ║
║   DNS Brute • API • Certificate     ║
╚══════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

usage() {
    echo "Usage: $0 -d <domain> [-w <wordlist>] [-t <threads>]"
    echo "  -d <domain>    Target domain (e.g., target.com)"
    echo "  -w <wordlist>  Subdomain wordlist"
    echo "  -t <threads>   Thread count"
    echo "  -h             Help"
    exit 1
}

DOMAIN=""
WORDLIST="wordlists/subdomains.txt"
THREADS=20

while getopts "d:w:t:h" opt; do
    case $opt in
        d) DOMAIN="$OPTARG" ;;
        w) WORDLIST="$OPTARG" ;;
        t) THREADS="$OPTARG" ;;
        h) usage ;;
        *) usage ;;
    esac
done

[[ -z "$DOMAIN" ]] && usage

banner
echo -e "${GREEN}[+] Domain: $DOMAIN"
echo -e "[+] Wordlist: $WORDLIST"
echo -e "[+] Threads: $THREADS${NC}\n"

# Create default wordlist if missing
if [[ ! -f "$WORDLIST" ]]; then
    echo -e "${YELLOW}[*] Creating default wordlist...${NC}"
    mkdir -p wordlists
    cat > "$WORDLIST" << 'EOF'
www
mail
admin
blog
api
dev
test
staging
vpn
smtp
pop3
imap
webmail
cpanel
whm
ns1
ns2
ns3
mx1
mx2
ftp
sftp
ssh
remote
gitlab
jenkins
jira
confluence
wiki
docs
support
helpdesk
ticket
portal
app
my
shop
store
cart
checkout
payment
gateway
secure
ssl
cdn
static
assets
media
img
images
css
js
download
upload
backup
db
database
redis
mongo
mysql
nginx
apache
tomcat
jboss
wildfly
kibana
elastic
grafana
prometheus
monitor
status
health
internal
private
corp
hr
payroll
erp
crm
analytics
tracking
logs
jenkins
sonar
nexus
artifactory
docker
k8s
kubernetes
swarm
rancher
cloud
vm
server
node
worker
master
prod
production
sandbox
demo
beta
alpha
news
forum
community
profile
user
account
login
auth
oauth
sso
ldap
radius
EOF
    echo -e "${GREEN}[✓] Created wordlist with 100+ entries${NC}"
fi

echo -e "${CYAN}[*] Starting subdomain enumeration...${NC}\n"

# Method 1: DNS brute force
echo -e "${YELLOW}[Method 1] DNS brute force${NC}"
found=0
while IFS= read -r sub; do
    [[ -z "$sub" ]] && continue
    fqdn="${sub}.${DOMAIN}"
    host "$fqdn" &>/dev/null && echo -e "${GREEN}[+] $fqdn${NC}" && ((found++))
done < "$WORDLIST"

# Method 2: crt.sh (Certificate Transparency)
echo -e "\n${YELLOW}[Method 2] crt.sh certificate search${NC}"
curl -s "https://crt.sh/?q=%25.${DOMAIN}&output=json" 2>/dev/null | \
    python3 -c "import sys,json; data=json.load(sys.stdin); [print(f'\033[0;32m[+] {x[\"name_value\"]}\033[0m') for x in data]" 2>/dev/null || \
    echo -e "${RED}[!] crt.sh lookup failed${NC}"

echo -e "\n${GREEN}[✓] Enumeration complete. Found subdomains.${NC}"
