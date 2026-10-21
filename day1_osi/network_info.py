"""
DAY 1 — OSI MODEL & TCP/IP STACK
Practical: See your own network info, trace a route, understand each layer
"""

import socket
import subprocess
import platform

def print_section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

# ── 1. Your Machine's Network Info ──────────────────
print_section("YOUR MACHINE NETWORK INFO")
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print(f"  Hostname   : {hostname}")
print(f"  Local IP   : {local_ip}")

# ── 2. DNS Resolution (Application Layer → Network Layer)
print_section("DNS RESOLUTION (Application -> Network Layer)")
domains = ["google.com", "github.com", "youtube.com"]
for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        print(f"  {domain:<20} → {ip}")
    except Exception as e:
        print(f"  {domain:<20} → ERROR: {e}")

# ── 3. Reverse DNS Lookup ────────────────────────────
print_section("REVERSE DNS LOOKUP (IP → Hostname)")
ips = ["8.8.8.8", "1.1.1.1", "142.250.182.14"]
for ip in ips:
    try:
        host = socket.gethostbyaddr(ip)[0]
        print(f"  {ip:<20} → {host}")
    except:
        print(f"  {ip:<20} → No reverse DNS found")

# ── 4. OSI Layer Reference ───────────────────────────
print_section("OSI MODEL REFERENCE — INTERVIEW CHEAT SHEET")
layers = [
    (7, "Application",  "HTTP, HTTPS, FTP, SMTP, DNS"),
    (6, "Presentation", "SSL/TLS, Encryption, Compression"),
    (5, "Session",      "NetBIOS, PPTP, Session management"),
    (4, "Transport",    "TCP, UDP — Ports live here"),
    (3, "Network",      "IP, ICMP, Routing — IP addresses"),
    (2, "Data Link",    "MAC addresses, Ethernet, WiFi frames"),
    (1, "Physical",     "Cables, Signals, Bits"),
]
print(f"  {'Layer':<8} {'Name':<16} {'Protocols'}")
print(f"  {'-'*60}")
for num, name, protocols in layers:
    print(f"  L{num:<7} {name:<16} {protocols}")

# ── 5. TCP/IP Stack Mapping ──────────────────────────
print_section("TCP/IP STACK (4-Layer Model)")
tcpip = [
    ("Application",  "HTTP, FTP, DNS, SMTP"),
    ("Transport",    "TCP, UDP"),
    ("Internet",     "IP, ICMP, ARP"),
    ("Network Access","Ethernet, WiFi, MAC"),
]
for layer, protocols in tcpip:
    print(f"  {layer:<18} → {protocols}")

print("\n✅ Day 1 complete! Run 'tracert google.com' in terminal to see live hops.\n")
