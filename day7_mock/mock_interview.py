"""
DAY 7 — MOCK INTERVIEW
Interactive Q&A + Coding Challenge.
One person runs this as interviewer, other person answers verbally.
Then swap roles!
"""

import random
import time
import socket

def print_header(title):
    print(f"\n{'#'*60}")
    print(f"  {title}")
    print(f"{'#'*60}\n")

def wait():
    input("\n  [Press Enter when ready to see answer...] ")

# ── SECTION 1: Rapid Fire Q&A ───────────────────────
print_header("ROUND 1 — RAPID FIRE Q&A")
print("  Rules: Answer out loud, then press Enter to see model answer.")
print("  Score yourself 0-2 for each answer.\n")

qa = [
    {
        "q": "Q1: What is a socket?",
        "a": """Answer: A socket is an endpoint of a network connection.
        It's identified by: IP Address + Port Number
        Example: 192.168.1.1:8080
        Think of it as a phone number (IP) + extension (Port).
        TCP socket = connected (like a phone call)
        UDP socket = connectionless (like sending a letter)"""
    },
    {
        "q": "Q2: What's the difference between TCP and UDP? Give real examples.",
        "a": """Answer:
        TCP — Reliable, ordered, connection-based
          - 3-way handshake (SYN → SYN-ACK → ACK)
          - Guarantees delivery and order
          - Examples: HTTP/HTTPS, email (SMTP), file transfer (FTP), SSH
          
        UDP — Fast, connectionless, no guarantee
          - No handshake, just fire datagrams
          - May arrive out of order or not at all
          - Examples: Video calls (Zoom), online gaming, DNS, live streaming
          
        Key insight: In video calls, a dropped frame is better than freezing
        to retransmit (that's why UDP!)"""
    },
    {
        "q": "Q3: Explain the full DNS resolution process for 'github.com'",
        "a": """Answer (full chain):
        1. Browser Cache — "Did I resolve this recently?"
        2. OS Cache — ipconfig /displaydns (Windows)
        3. hosts file — C:\\Windows\\System32\\drivers\\etc\\hosts
        4. Recursive Resolver (your ISP/Google/Cloudflare)
        5. Root Name Server (13 globally, knows all TLD servers)
        6. .com TLD Server — "Who handles github.com?"
        7. GitHub's Authoritative DNS — "github.com = 140.82.121.4"
        8. Answer cached with TTL, then browser connects!"""
    },
    {
        "q": "Q4: What is the difference between HTTP 401 and 403?",
        "a": """Answer:
        401 Unauthorized — "I don't know WHO you are"
          - Not authenticated, need to log in
          - Fix: Send credentials (token, username/password)
          
        403 Forbidden — "I know who you are, but NO"
          - Authenticated but not authorized
          - Fix: Need different permissions/role
          
        Real example:
          401 = Trying to access /admin without logging in
          403 = Logged in as regular user, trying to access /admin"""
    },
    {
        "q": "Q5: What is a 502 Bad Gateway vs 503 Service Unavailable?",
        "a": """Answer:
        502 Bad Gateway:
          - The server (acting as gateway/proxy) got bad response from upstream
          - Example: Your Load Balancer can't reach the backend server
          - Fix: Check backend server health
          
        503 Service Unavailable:
          - Server is temporarily unable to handle requests
          - Usually: overloaded or down for maintenance
          - Often includes Retry-After header
          
        Quick memory trick:
          502 = gateway problem (backend sent garbage)
          503 = server problem (backend is dead/busy)"""
    },
    {
        "q": "Q6: What happens at each step when you type https://google.com in browser?",
        "a": """Answer (full URL-to-page journey):
        1.  URL Parse: scheme=https, host=google.com, port=443
        2.  DNS Lookup: google.com → 142.250.x.x
        3.  TCP Connect: SYN → SYN-ACK → ACK (3-way handshake) to port 443
        4.  TLS Handshake: Exchange certificates, agree on cipher, symmetric key
        5.  HTTP Request: GET / HTTP/1.1, Host: google.com, cookies, etc.
        6.  Server Processing: Routes to handler, queries DB if needed
        7.  HTTP Response: 200 OK + HTML body
        8.  Browser Parsing: Parse HTML, find <img>, <script>, <link> tags
        9.  Parallel Requests: Fetch CSS, JS, images (HTTP/2 multiplexing!)
        10. Render: Build DOM + CSSOM → Render Tree → Layout → Paint"""
    },
    {
        "q": "Q7: What is Load Balancing? Name 3 algorithms.",
        "a": """Answer:
        Load Balancing = distributing incoming traffic across multiple servers
        Goal: No single server gets overwhelmed, high availability
        
        Algorithms:
        1. Round Robin — requests go to servers in rotation (1→2→3→1→2→3)
           Simple, works when all servers have equal capacity
           
        2. Least Connections — send to server with fewest active connections
           Better when requests have varying processing times
           
        3. IP Hash — client IP → always same server (sticky session)
           Needed when server stores session state
           
        Bonus: Weighted Round Robin — Server A gets 2x traffic vs Server B
        (when servers have different hardware specs)"""
    },
    {
        "q": "Q8: What OSI layer does HTTP operate on? What about TCP? IP? Ethernet?",
        "a": """Answer:
        Layer 7 — Application:  HTTP, HTTPS, FTP, SMTP, DNS
        Layer 6 — Presentation: TLS/SSL, encryption, compression
        Layer 5 — Session:      Session management, NetBIOS
        Layer 4 — Transport:    TCP, UDP (PORTS live here!)
        Layer 3 — Network:      IP, ICMP, routing (IP ADDRESSES live here!)
        Layer 2 — Data Link:    Ethernet, WiFi (MAC ADDRESSES live here!)
        Layer 1 — Physical:     Cables, signals, bits
        
        Memory trick: "All People Seem To Need Data Processing"
        (Application, Presentation, Session, Transport, Network, Data, Physical)"""
    },
]

scores = []
for i, item in enumerate(qa):
    print(f"  {item['q']}")
    wait()
    print(f"\n  ✅ MODEL ANSWER:")
    for line in item['a'].split('\n'):
        print(f"  {line}")
    score = input("\n  Your score (0=missed, 1=partial, 2=nailed it): ")
    try:
        scores.append(int(score))
    except:
        scores.append(1)
    print(f"  {'─'*50}")

total = sum(scores)
max_score = len(qa) * 2
print(f"\n  {'='*50}")
print(f"  ROUND 1 SCORE: {total}/{max_score} ({total/max_score*100:.0f}%)")
if total/max_score >= 0.8:
    print("  🏆 Excellent! You're interview-ready on these topics!")
elif total/max_score >= 0.6:
    print("  📚 Good! Review the ones you missed and redo tomorrow.")
else:
    print("  💪 Keep practicing! Revisit Days 1-6 scripts.")
print(f"  {'='*50}")

# ── SECTION 2: Live Coding Challenge ────────────────
print_header("ROUND 2 — LIVE CODING CHALLENGE")
print("  Task: Write a TCP echo server that UPPERCASES everything the client sends.")
print("  Time limit: 10 minutes. No Google, no notes!\n")
print("  Requirements:")
print("    1. Listen on port 5555")
print("    2. Accept one client connection")
print("    3. Receive messages from client")
print("    4. Send back the UPPERCASE version")
print("    5. Loop until client sends 'quit'\n")
print("  Start coding now... Press Enter when done.\n")

input("  [Press Enter when you're done coding to see the solution...]\n")

print("""
  ✅ SOLUTION:

  import socket
  
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(('localhost', 5555))
  server.listen(1)
  print("Waiting for connection...")
  
  conn, addr = server.accept()
  print(f"Connected: {addr}")
  
  while True:
      data = conn.recv(1024)
      if not data or data.decode().strip() == 'quit':
          break
      response = data.decode().upper()
      conn.send(response.encode())
  
  conn.close()
  server.close()
""")

# ── SECTION 3: Whiteboard Question ──────────────────
print_header("ROUND 3 — WHITEBOARD ARCHITECTURE")
print("  Draw this on paper (5 minutes):")
print("""
  Design the network flow for:
  "User visits amazon.com, searches for 'laptop', and places an order"
  
  Must include:
    - DNS resolution
    - CDN layer  
    - Load Balancer
    - Web Servers
    - Database
    - Cache (Redis)
    - Payment service
  
  Draw arrows showing request/response flow!
""")

wait()

print("""
  ✅ MODEL ARCHITECTURE:

  User Browser
      │
      ▼ DNS lookup: amazon.com → CDN IP
  [CDN - CloudFront]  ←── Static assets cached here (JS, CSS, images)
      │ (cache miss for dynamic content)
      ▼
  [Load Balancer]  ←── Distributes traffic, health checks backends
      │
      ├──→ [Web Server 1]
      ├──→ [Web Server 2]   ←── Stateless, handles HTTP requests
      └──→ [Web Server 3]
                │
                ├──→ [Redis Cache]  ←── Session data, frequent queries
                │
                ├──→ [Product DB]   ←── Product catalog, inventory
                │
                ├──→ [User DB]      ←── User accounts, addresses
                │
                └──→ [Order Service] → [Payment API (Stripe/Razorpay)]
                                              │
                                        [Payment DB]

  Key discussion points:
    - CDN reduces latency for static content globally
    - Load Balancer provides high availability  
    - Redis caching reduces DB load by ~80%
    - Payment service is separate for security (PCI compliance)
    - Each service can scale independently!
""")

print_header("🎉 MOCK INTERVIEW COMPLETE!")
print("  Swap roles and do it again!")
print("  The person who was answering becomes the interviewer.\n")
print("  Final tips for real interviews:")
print("  ✓ Always think out loud — interviewers want to see your process")
print("  ✓ Ask clarifying questions before jumping to solution")
print("  ✓ Start simple, then add complexity")
print("  ✓ Mention trade-offs (TCP vs UDP, not just 'use TCP')")
print("  ✓ Say 'In production, I'd also consider...' — shows depth\n")
