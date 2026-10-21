"""
DAY 3 — DNS DEEP DIVE
Practical: Full DNS resolution, reverse lookup, record types, TTL, speed comparison
"""

import socket
import time
import subprocess

def print_section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

# ── 1. Forward DNS Resolution ────────────────────────
print_section("1. FORWARD DNS LOOKUP (Domain → IP)")
domains = ["google.com", "github.com", "stackoverflow.com", "youtube.com"]
for domain in domains:
    try:
        start = time.time()
        ip = socket.gethostbyname(domain)
        elapsed = (time.time() - start) * 1000
        print(f"  {domain:<30} → {ip:<20} ({elapsed:.2f}ms)")
    except Exception as e:
        print(f"  {domain:<30} → FAILED: {e}")

# ── 2. Reverse DNS Lookup ────────────────────────────
print_section("2. REVERSE DNS LOOKUP (IP → Domain)")
ips = {
    "8.8.8.8":  "Google Public DNS",
    "1.1.1.1":  "Cloudflare DNS",
    "8.8.4.4":  "Google Secondary DNS",
}
for ip, description in ips.items():
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print(f"  {ip:<20} → {hostname} ({description})")
    except:
        print(f"  {ip:<20} → No PTR record found ({description})")

# ── 3. Multiple IPs for one domain (DNS Load Balancing)
print_section("3. DNS LOAD BALANCING (One domain → Multiple IPs)")
try:
    results = socket.getaddrinfo("google.com", 80)
    ips_found = list(set([r[4][0] for r in results]))
    print(f"  google.com resolves to {len(ips_found)} IPs:")
    for ip in ips_found[:5]:
        print(f"    → {ip}")
    print("  (Google rotates these for load balancing!)")
except Exception as e:
    print(f"  Error: {e}")

# ── 4. DNS Caching Demo ──────────────────────────────
print_section("4. DNS CACHING EFFECT")
domain = "github.com"
print(f"  Testing caching effect for '{domain}':")
times = []
for i in range(3):
    start = time.time()
    socket.gethostbyname(domain)
    elapsed = (time.time() - start) * 1000
    times.append(elapsed)
    print(f"    Attempt {i+1}: {elapsed:.3f}ms")

print(f"  First call: {times[0]:.3f}ms (cache miss — went to DNS server)")
if times[1] < times[0]:
    print(f"  Later calls: faster due to OS/browser caching")

# ── 5. DNS Resolution Chain Explanation ─────────────
print_section("5. DNS RESOLUTION CHAIN (Interview Gold!)")
chain = [
    ("Step 1", "Browser Cache",     "Did I already look this up recently?"),
    ("Step 2", "OS Cache",          "ipconfig /displaydns — already resolved?"),
    ("Step 3", "hosts file",        "C:\\Windows\\System32\\drivers\\etc\\hosts"),
    ("Step 4", "Router/ISP DNS",    "Your local DNS resolver"),
    ("Step 5", "Root DNS Server",   "13 root servers worldwide — knows TLD servers"),
    ("Step 6", ".com TLD Server",   "Knows authoritative server for google.com"),
    ("Step 7", "Authoritative DNS", "google.com's own DNS — final answer!"),
]
for step, where, description in chain:
    print(f"  {step}: {where:<25} — {description}")

# ── 6. Record Types Reference ───────────────────────
print_section("6. DNS RECORD TYPES (Must Know for Interviews)")
records = [
    ("A",     "Maps domain to IPv4 address",          "google.com → 142.250.x.x"),
    ("AAAA",  "Maps domain to IPv6 address",           "google.com → 2607:f8b0::..."),
    ("CNAME", "Alias — one domain to another domain",  "www.github.com → github.com"),
    ("MX",    "Mail server for the domain",            "gmail.com → aspmx.l.google.com"),
    ("TXT",   "Arbitrary text (used for SPF, DKIM)",   "v=spf1 include:google.com"),
    ("NS",    "Nameservers for the domain",            "google.com → ns1.google.com"),
    ("PTR",   "Reverse lookup (IP → hostname)",        "8.8.8.8 → dns.google"),
    ("SOA",   "Start of Authority — zone info",        "Serial, refresh, retry times"),
]
print(f"  {'Type':<8} {'Purpose':<42} {'Example'}")
print(f"  {'-'*80}")
for rtype, purpose, example in records:
    print(f"  {rtype:<8} {purpose:<42} {example}")

print("\n✅ Day 3 complete! Also run 'nslookup -type=MX gmail.com' in terminal!\n")
