# 🌐 Networking Week — Interview Preparation Guide

> A week-long practical networking study plan for interview preparation.
> Each day covers one core topic with hands-on Python scripts and real commands.

---

## 📁 Project Structure

```
networking-week/
├── day1_osi/
│   └── network_info.py          ← OSI layers, DNS lookup, network info
├── day2_tcp_udp/
│   ├── tcp_server.py            ← TCP server (3-way handshake demo)
│   ├── tcp_client.py            ← TCP client
│   ├── udp_server.py            ← UDP server (connectionless demo)
│   └── udp_client.py            ← UDP client
├── day3_dns/
│   └── dns_deep_dive.py         ← DNS resolution, caching, record types
├── day4_http/
│   ├── http_server.py           ← REST API server (GET/POST/PUT/DELETE)
│   └── http_client.py           ← Tests all API endpoints
├── day5_sockets/
│   ├── chat_server.py           ← Multi-client threaded chat server
│   └── chat_client.py           ← Chat client
├── day6_loadbalancer/
│   └── load_balancer.py         ← Round Robin LB + 3 backend servers
├── day7_mock/
│   └── mock_interview.py        ← Interactive Q&A + coding challenge
└── README.md                    ← This file
```

---

## ▶️ How to Run

| Day | Command | Terminals |
|-----|---------|-----------|
| Day 1 | `python day1_osi/network_info.py` | 1 |
| Day 2 TCP | Terminal 1: `python day2_tcp_udp/tcp_server.py` → Terminal 2: `python day2_tcp_udp/tcp_client.py` | 2 |
| Day 2 UDP | Terminal 1: `python day2_tcp_udp/udp_server.py` → Terminal 2: `python day2_tcp_udp/udp_client.py` | 2 |
| Day 3 | `python day3_dns/dns_deep_dive.py` | 1 |
| Day 4 | Terminal 1: `python day4_http/http_server.py` → Terminal 2: `python day4_http/http_client.py` | 2 |
| Day 5 | Terminal 1: `python day5_sockets/chat_server.py` → Terminal 2 & 3: `python day5_sockets/chat_client.py` | 3 |
| Day 6 | `python day6_loadbalancer/load_balancer.py` | 1 |
| Day 7 | `python day7_mock/mock_interview.py` | 1 |

---

## 📅 Day 1 — OSI Model & TCP/IP Stack

### What We Learned
The OSI model has **7 layers**. Every network request passes through these layers.

| Layer | Name | Protocols | Real Life Analogy |
|-------|------|-----------|-------------------|
| L7 | Application | HTTP, HTTPS, DNS, FTP | The app you use (browser) |
| L6 | Presentation | SSL/TLS, Encryption | Translator / Encoder |
| L5 | Session | NetBIOS, PPTP | Managing the conversation |
| L4 | Transport | TCP, UDP | Delivery method (courier) |
| L3 | Network | IP, ICMP | City address (IP address) |
| L2 | Data Link | Ethernet, WiFi, MAC | Street address (MAC address) |
| L1 | Physical | Cables, Signals | The actual road |

> **Memory Trick:** "All People Seem To Need Data Processing"
> (Application → Presentation → Session → Transport → Network → Data Link → Physical)

### Key Concepts

**Hostname** — Your computer's name on the network (e.g. `DESKTOP-S0BCQ6L`)

**Local IP (Private IP)** — e.g. `192.168.76.216`
- Only works inside your home/office network
- Assigned by router using **DHCP**
- Think: your flat number inside a building

**Public IP** — Assigned by your ISP
- Visible to the whole internet
- Think: your building's street address

**DNS Resolution** — Converts domain name to IP
```
google.com  →  172.217.26.110
github.com  →  20.207.73.82
youtube.com →  142.251.106.91
```

**Reverse DNS** — Converts IP back to domain name
```
8.8.8.8   →  dns.google       (Google's public DNS)
1.1.1.1   →  one.one.one.one  (Cloudflare's public DNS)
```

### Terminal Commands
```powershell
ipconfig /all                    # see your IP, gateway, DNS
tracert google.com               # trace packet hops to google
ping google.com                  # test connectivity (ICMP)
nslookup google.com              # forward DNS lookup
nslookup 8.8.8.8                 # reverse DNS lookup
nslookup google.com 1.1.1.1      # use Cloudflare's DNS server
```

### Interview Questions
| Question | Answer |
|----------|--------|
| What is DNS? | Converts domain names to IP addresses (phonebook of internet) |
| What is `192.168.x.x`? | Private IP, assigned by router via DHCP |
| What is `8.8.8.8`? | Google's public DNS server |
| What layer does DNS work on? | Layer 7 — Application Layer |
| What layer does IP work on? | Layer 3 — Network Layer |
| Private vs Public IP? | Private = inside network only, Public = visible on internet |

---

## 📅 Day 2 — TCP vs UDP

### What We Learned

#### TCP (Transmission Control Protocol)
- **Reliable** — guarantees delivery
- **Ordered** — packets arrive in order
- **Connection-based** — requires 3-way handshake before data transfer
- Uses: HTTP, HTTPS, Email, File Transfer, SSH

#### The 3-Way Handshake (TCP Connection Setup)
```
Client          Server
  |--- SYN ------->|   "Hey, can we talk?"
  |<-- SYN-ACK ----|   "Sure, I'm ready!"
  |--- ACK ------->|   "Great, let's go!"
  |                |
  |=== DATA ======>|   (actual communication starts)
  |                |
  |--- FIN ------->|   "I'm done, bye!"
  |<-- FIN-ACK ----|   "Ok, bye!"
  |--- ACK ------->|   "Confirmed, closing."
```

#### UDP (User Datagram Protocol)
- **Fast** — no connection setup
- **No guarantee** — packets may be lost or arrive out of order
- **Connectionless** — just fire and forget
- Uses: Video calls (Zoom), Online gaming, DNS, Live streaming

#### TCP vs UDP Comparison
| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Yes (3-way handshake) | No |
| Reliability | Guaranteed delivery | No guarantee |
| Order | Ordered | May be out of order |
| Speed | Slower (overhead) | Faster |
| Use case | Web, email, file transfer | Video calls, gaming, DNS |

> **Interview Gold:** "In video calls, a dropped frame is better than freezing
> to wait for retransmission — that's why we use UDP!"

### Terminal Commands
```powershell
netstat -ano                     # see all TCP/UDP connections
netstat -ano | findstr :443      # filter HTTPS connections
netstat -ano | findstr LISTENING # what ports your machine is serving
```

### Interview Questions
| Question | Answer |
|----------|--------|
| What is the 3-way handshake? | SYN → SYN-ACK → ACK (establishes TCP connection) |
| Why use UDP for video calls? | Speed over reliability — dropped frame better than freeze |
| Is DNS TCP or UDP? | UDP (port 53) — fast lookup, no connection needed |
| What port does HTTPS use? | 443 (TCP) |
| What port does HTTP use? | 80 (TCP) |

---

## 📅 Day 3 — DNS Deep Dive

### What We Learned

#### Full DNS Resolution Chain
When you type `google.com`, this happens in order:

```
Step 1: Browser Cache        → "Did I resolve this recently?"
Step 2: OS Cache             → ipconfig /displaydns (Windows)
Step 3: hosts file           → C:\Windows\System32\drivers\etc\hosts
Step 4: Router / ISP DNS     → Your local DNS resolver
Step 5: Root Name Server     → 13 root servers worldwide
Step 6: .com TLD Server      → Knows who handles google.com
Step 7: Google's Auth DNS    → "google.com = 172.217.26.110"
```

#### DNS Record Types (Must Know!)
| Type | Purpose | Example |
|------|---------|---------|
| A | Domain → IPv4 address | `google.com → 142.250.x.x` |
| AAAA | Domain → IPv6 address | `google.com → 2607:f8b0::...` |
| CNAME | Alias (domain → domain) | `www.github.com → github.com` |
| MX | Mail server for domain | `gmail.com → aspmx.l.google.com` |
| TXT | Text info (SPF, DKIM) | `v=spf1 include:google.com` |
| NS | Nameservers for domain | `google.com → ns1.google.com` |
| PTR | Reverse lookup (IP → hostname) | `8.8.8.8 → dns.google` |

#### What is TTL?
- **TTL = Time To Live**
- How long a DNS answer is **cached** before asking again
- Example: TTL = 300 → cached for 5 minutes
- Lower TTL = faster propagation of changes (but more DNS queries)
- Higher TTL = less DNS traffic (but slower to update)

#### DNS Load Balancing
One domain can map to **multiple IPs**:
```
google.com → 142.250.x.x
           → 142.251.x.x
           → 172.217.x.x
```
Google rotates these so no single server gets all traffic!

### Terminal Commands
```powershell
nslookup google.com              # A record (IPv4)
nslookup -type=MX gmail.com      # MX record (mail servers)
nslookup -type=CNAME www.github.com  # CNAME record
ipconfig /flushdns               # clear DNS cache
ipconfig /displaydns             # see cached DNS entries
```

### Interview Questions
| Question | Answer |
|----------|--------|
| What is DNS TTL? | How long to cache a DNS result before re-querying |
| What is a CNAME record? | Alias — maps one domain to another domain |
| What is a MX record? | Mail Exchange — points to email server for a domain |
| Why does google.com have multiple IPs? | DNS-based load balancing |
| What is `ipconfig /flushdns`? | Clears the local DNS cache |

---

## 📅 Day 4 — HTTP/HTTPS & REST

### What We Learned

#### HTTP Methods
| Method | Purpose | Idempotent? | Example |
|--------|---------|------------|---------|
| GET | Read data | Yes | Fetch user profile |
| POST | Create new resource | No | Create new user |
| PUT | Update/replace resource | Yes | Update user info |
| DELETE | Remove resource | Yes | Delete a user |
| PATCH | Partial update | No | Update only email |

> **Idempotent** = calling it multiple times gives same result.
> DELETE /users/1 ten times = same as calling it once (user is deleted).
> POST /users ten times = creates 10 users! (not idempotent)

#### HTTP Status Codes (Must Know!)
```
2xx → Success
  200 OK                  → Request successful
  201 Created             → New resource created (use after POST)
  204 No Content          → Success but no body (use after DELETE)

3xx → Redirection
  301 Moved Permanently   → URL changed forever (update bookmarks)
  302 Found               → Temporary redirect

4xx → Client Error (YOUR fault)
  400 Bad Request         → Malformed request syntax
  401 Unauthorized        → Not logged in (who are you?)
  403 Forbidden           → Logged in but no permission (wrong role)
  404 Not Found           → Resource doesn't exist
  429 Too Many Requests   → Rate limited (slow down!)

5xx → Server Error (SERVER's fault)
  500 Internal Server Error → Something broke on the server
  502 Bad Gateway           → Server got bad response from upstream
  503 Service Unavailable   → Server overloaded or down for maintenance
```

#### HTTP vs HTTPS
```
HTTP  → Port 80  → Plain text (anyone can read your data!)
HTTPS → Port 443 → Encrypted with TLS (safe!)
```

#### TLS Handshake (HTTPS)
```
1. Client Hello    → "I support TLS 1.3, here are my cipher suites"
2. Server Hello    → "Let's use AES-256, here's my certificate"
3. Certificate     → Server proves its identity (signed by CA)
4. Key Exchange    → Agree on a symmetric encryption key
5. Encrypted Data  → All communication now encrypted!
```

### Terminal Commands
```powershell
curl http://localhost:8080/              # GET request
curl http://localhost:8080/users        # list users
curl -X POST http://localhost:8080/users -H "Content-Type: application/json" -d '{"name":"Alice"}'
curl -X DELETE http://localhost:8080/users/1
curl -v https://google.com              # verbose — see TLS handshake!
curl -I https://google.com              # headers only
```

### Interview Questions
| Question | Answer |
|----------|--------|
| 401 vs 403? | 401 = not authenticated, 403 = authenticated but no permission |
| 200 vs 201? | 200 = OK, 201 = resource created (use after POST) |
| 502 vs 503? | 502 = bad response from upstream, 503 = server unavailable |
| What is HTTPS? | HTTP + TLS encryption on port 443 |
| What is idempotent? | Same result no matter how many times you call it |
| PUT vs PATCH? | PUT = replace whole resource, PATCH = update part of resource |

---

## 📅 Day 5 — Sockets & Ports

### What We Learned

#### What is a Socket?
- A socket = **IP Address + Port Number**
- It's the endpoint of a network connection
- Example: `192.168.76.216:8080`
- Think of it as: IP = building address, Port = flat/room number

#### Well-Known Ports (Must Memorize!)
| Port | Protocol | Use |
|------|---------|-----|
| 22 | SSH | Secure remote login |
| 25 | SMTP | Sending emails |
| 53 | DNS | Domain name resolution (UDP) |
| 80 | HTTP | Web traffic (unencrypted) |
| 443 | HTTPS | Web traffic (encrypted) |
| 3306 | MySQL | MySQL database |
| 5432 | PostgreSQL | PostgreSQL database |
| 6379 | Redis | Redis cache |
| 27017 | MongoDB | MongoDB database |
| 8080 | HTTP Alt | Common dev server port |

#### How Multiple Clients Work (Threading)
```
Server listens on port 7777
    │
    ├── Client 1 connects → Thread 1 handles Client 1
    ├── Client 2 connects → Thread 2 handles Client 2
    └── Client 3 connects → Thread 3 handles Client 3

Each client gets its OWN thread = parallel handling!
```

### Terminal Commands
```powershell
netstat -ano                          # all connections + PID
netstat -ano | findstr :8080          # what's on port 8080
netstat -ano | findstr LISTENING      # all listening ports
tasklist | findstr <PID>              # find process by PID
```

### Interview Questions
| Question | Answer |
|----------|--------|
| What is a socket? | Endpoint of a connection = IP + Port |
| What port does MySQL use? | 3306 |
| What port does SSH use? | 22 |
| How does a server handle multiple clients? | Threading (one thread per client) |
| What is `netstat`? | Shows all active network connections |

---

## 📅 Day 6 — Load Balancing & CDN

### What We Learned

#### What is Load Balancing?
Distributing incoming traffic across multiple servers so:
- No single server gets overwhelmed
- High availability (if one server dies, others handle traffic)
- Better performance for users

#### Load Balancing Algorithms
| Algorithm | How It Works | Best For |
|-----------|-------------|---------|
| Round Robin | Requests go to servers in rotation: 1→2→3→1→2→3 | Equal capacity servers |
| Least Connections | Send to server with fewest active connections | Requests with varying processing time |
| IP Hash | Client IP always maps to same server (sticky) | When session state is on server |
| Weighted Round Robin | Server A gets 2x traffic vs Server B | Servers with different specs |

#### Architecture Diagram
```
Client
   |
   ▼
[Load Balancer :9000]
   |
   ├──→ [Backend Server 1 :8001]
   ├──→ [Backend Server 2 :8002]
   └──→ [Backend Server 3 :8003]
              |
              ▼
         [Database]
```

#### What is a CDN?
- **CDN = Content Delivery Network**
- Servers spread across the world that cache static content
- User gets content from the nearest server = faster!
- Examples: Cloudflare, AWS CloudFront, Akamai

```
Without CDN: User in India → Server in USA (high latency!)
With CDN:    User in India → CDN server in Mumbai (fast!)
```

#### What are Sticky Sessions?
- Problem: User logs in on Server 1, next request goes to Server 2 (session lost!)
- Solution: **Sticky Session** — always route same user to same server
- Done via IP Hash or session cookies
- Downside: uneven load distribution

### Discussion Questions
- What happens if Backend Server 2 goes down?
- How would you add health checks to the load balancer?
- When would you use Least Connections over Round Robin?
- How does Netflix handle millions of simultaneous streams?

### Interview Questions
| Question | Answer |
|----------|--------|
| What is a Load Balancer? | Distributes traffic across multiple servers |
| What is Round Robin? | Each request goes to next server in rotation |
| What is a Sticky Session? | User always routed to same server |
| What is a CDN? | Globally distributed servers that cache static content |
| What is a health check? | LB pings servers regularly to detect failures |

---

## 📅 Day 7 — Mock Interview

### The Ultimate Interview Question

> **"Walk me through what happens when you type `https://google.com` in your browser"**

```
1.  URL Parse         → scheme=https, host=google.com, port=443

2.  Browser Cache     → Already resolved google.com? Use cached IP

3.  DNS Lookup        → OS cache → Router → ISP DNS → Root → .com → Google DNS
                     → google.com = 172.217.26.110

4.  TCP Connect       → SYN → SYN-ACK → ACK  (3-way handshake to port 443)

5.  TLS Handshake     → Exchange certificates, agree on encryption key

6.  HTTP Request      → GET / HTTP/1.1
                        Host: google.com
                        Cookie: ...
                        User-Agent: Chrome/...

7.  Server Processing → Routes request, checks cache, queries DB if needed

8.  HTTP Response     → 200 OK + HTML body

9.  Browser Parses    → Finds <img>, <link>, <script> tags

10. Parallel Fetches  → Downloads CSS, JS, images (HTTP/2 multiplexing)

11. Render            → DOM + CSSOM → Render Tree → Layout → Paint → Done!
```

### System Design: Amazon Architecture
```
User → CDN (static files: images, CSS, JS)
     → Load Balancer
         → Web Server 1 ──→ Redis Cache
         → Web Server 2 ──→ Product DB
         → Web Server 3 ──→ User DB
                        ──→ Order Service → Payment API
```

### Rapid Fire Answers
| Q | A |
|---|---|
| TCP vs UDP? | TCP = reliable+ordered, UDP = fast+no guarantee |
| What is DNS TTL? | How long to cache a DNS answer |
| 401 vs 403? | 401 = not logged in, 403 = logged in but no access |
| 502 vs 503? | 502 = bad upstream response, 503 = server down |
| What layer is HTTP? | Layer 7 — Application |
| What is a socket? | IP + Port = endpoint of a connection |
| What is Round Robin? | Requests distributed to servers in rotation |
| What is a CDN? | Globally cached servers close to users |

---

## 🛠️ Tools Used This Week

| Tool | Purpose | Command |
|------|---------|---------|
| `ipconfig /all` | See network info | PowerShell |
| `ping` | Test connectivity (ICMP) | `ping google.com` |
| `tracert` | Trace packet route | `tracert google.com` |
| `nslookup` | DNS lookup | `nslookup google.com` |
| `netstat` | Active connections | `netstat -ano` |
| `curl` | HTTP requests | `curl http://localhost:8080` |
| `Wireshark` | Packet capture (GUI) | Install from wireshark.org |
| Python `socket` | Build TCP/UDP apps | stdlib — no install needed |

---

## 📚 Key Takeaways

1. **OSI Model** — 7 layers, each has a specific job. Ports live at Layer 4, IPs at Layer 3.
2. **TCP** — Reliable, ordered, 3-way handshake. Use for web, email, files.
3. **UDP** — Fast, no guarantee. Use for video calls, gaming, DNS.
4. **DNS** — Phonebook of internet. 7-step resolution chain. TTL controls caching.
5. **HTTP** — Request/Response protocol. Know your status codes (401 vs 403, 502 vs 503).
6. **Sockets** — IP + Port = unique connection endpoint.
7. **Load Balancing** — Distribute traffic. Round Robin, Least Connections, IP Hash.
8. **CDN** — Cache content globally, reduce latency.

---

*Prepared during Networking Week — Daily Standup Interview Prep 🚀*
