# Day 2 Networking — Interview Preparation Guide

**For:** Software Development Engineers (SDE / Backend) preparing for technical interviews.
**Prerequisite:** Complete [Day 1](./DAY1_INTERVIEW_GUIDE.md) first — this guide builds directly on it.

---

## Learning Outcomes

By the end of Day 2 you will be able to:

- Explain how HTTP/2 improves on HTTP/1.1 and why it matters for performance.
- Explain what WebSockets are, how they work, and when to use them instead of HTTP.
- Design clean, consistent REST APIs and explain your design choices.
- Explain CORS — what it is, why it exists, and how to configure it correctly.
- Compare JWT and session-based authentication and choose the right one.
- Explain what HTTP caching is and how `Cache-Control` works.
- Describe how backend services communicate with each other.

---

## Prerequisites

- Day 1 complete: you understand TCP, HTTP, DNS, IP addresses, and the client–server model.
- You have built at least one REST API endpoint.
- You know what a request header and response header are.

---

## Estimated Study Time

| Activity | Time |
|---|---|
| Reading and understanding the concepts | 2.5 – 3 hours |
| Practical exercises | 40 minutes |
| Reviewing interview answers | 30 minutes |
| **Total** | **~4.5 hours** |

---

## Table of Contents

1. [Scope: What is covered today and what is deferred](#scope)
2. [HTTP/1.1 vs HTTP/2](#1-http11-vs-http2)
3. [WebSockets](#2-websockets)
4. [REST API Design](#3-rest-api-design)
5. [CORS — Cross-Origin Resource Sharing](#4-cors--cross-origin-resource-sharing)
6. [Authentication: JWT vs Sessions](#5-authentication-jwt-vs-sessions)
7. [HTTP Caching and Cache-Control](#6-http-caching-and-cache-control)
8. [Service-to-Service Communication](#7-service-to-service-communication)
9. [Practical Exercises](#8-practical-exercises)
10. [Quick Reference Tables](#9-quick-reference-tables)
11. [Final Interview Prep: 12 Must-Know Q&A](#10-final-interview-prep)

---

## Scope

| Topic | Status | Notes |
|---|---|---|
| HTTP/2 vs HTTP/1.1 (multiplexing, compression) | Today | Frequently asked in SDE interviews |
| WebSockets — what, why, when | Today | Real-time systems question |
| REST API design principles | Today | You write APIs every day |
| CORS — what it is and how to fix it | Today | Every frontend-backend team hits this |
| JWT vs Session authentication | Today | Asked in almost every interview |
| HTTP caching and Cache-Control | Today | System design and performance |
| Service-to-service communication | Today | Microservices foundation |
| HTTP/3 and QUIC | 🔜 Later | Built on UDP, worth learning after HTTP/2 |
| OAuth 2.0 and OpenID Connect internals | 🔜 Later | Deep auth — Day 4 or 5 |
| GraphQL vs REST internals | 🔜 Later | Separate session |
| gRPC | 🔜 Later | Service communication — Day 3 |
| Message queues (Kafka, RabbitMQ) | 🔜 Later | Async communication — later sessions |
| TLS certificate internals | 🔜 Later | Too deep for interview prep |

---

## 1. HTTP/1.1 vs HTTP/2

### A. Interview-ready definition

**HTTP/1.1** processes one request at a time per TCP connection, which forces browsers to open multiple parallel connections to load a page with many resources. **HTTP/2** allows multiple requests and responses to be sent simultaneously over a single TCP connection (called **multiplexing**), compresses headers, and supports server push — significantly improving page load performance without changing how developers write HTTP.

### B. Explanation in simple language

In Day 1 you learned that HTTP is a request-response protocol. Let us look at the problem with HTTP/1.1 when a browser loads a typical page.

**The HTTP/1.1 problem: Head-of-line blocking**

When a browser loads `shop.example`, the HTML references 30 resources: 5 CSS files, 10 JavaScript files, 15 images. With HTTP/1.1:

- Each request must wait for the previous response to finish on that connection.
- Browsers work around this by opening 6 simultaneous TCP connections to the same server.
- But 6 connections × handshake overhead = significant wasted time.
- Large resources block smaller ones behind them in the queue.

This problem is called **head-of-line blocking** — one slow resource blocks everything behind it, like a slow car at the front of a single-lane road.

**HTTP/2: Multiple lanes on the same road**

HTTP/2 introduces **streams** — independent channels within one TCP connection. Each request gets its own stream. Responses can arrive in any order. A slow image response does not block a fast CSS response.

```
HTTP/1.1 on one connection:
[Request A]──────[Response A]──────[Request B]──────[Response B]

HTTP/2 on one connection (multiplexing):
[Request A]──────────────────────────[Response A (large)]
[Request B]────────[Response B (small, arrives first)]
[Request C]──[Response C (tiny, arrives immediately)]
```

### C. Why HTTP/2 exists

HTTP/1.1 was designed in 1997 when a typical web page had 5–10 resources. Modern pages have 50–200. HTTP/1.1's one-request-at-a-time model scales poorly. HTTP/2 was designed specifically to solve this at the protocol level without requiring application code changes.

### D. Real-life analogy

**HTTP/1.1** is a single checkout lane at a supermarket. Each customer (request) must wait for the one in front to finish, even if they only have one item.

**HTTP/2** is a checkout lane where the cashier can process multiple customers simultaneously, sending the receipt for the fast customer immediately without waiting for the slow customer's large trolley to finish.

Where the analogy breaks down: HTTP/2 still uses one TCP connection, so TCP-level packet loss affects all streams simultaneously (this is why HTTP/3 was built on UDP instead).

### E. Practical software example

Your ShopEasy product listing page loads:
- 1 HTML file
- 3 CSS files
- 8 JavaScript files
- 20 product images

**With HTTP/1.1:** The browser opens 6 TCP connections (6 handshakes) and sends requests in batches. Some requests queue behind slower ones.

**With HTTP/2:** One TCP connection. One TLS handshake. All 32 resources requested in parallel. The server responds to each as it is ready. Total load time drops significantly, especially on high-latency connections (mobile networks).

**As a backend developer:** You typically enable HTTP/2 at the load balancer or reverse proxy (Nginx, Caddy, AWS ALB) — not in your application code. Your Node.js or Python code does not change.

### F. HTTP/2 Key Features

**1. Multiplexing**
Multiple request/response pairs over one TCP connection. Covered above.

**2. Header Compression (HPACK)**

In HTTP/1.1, headers are sent as plain text with every request. Consider this: every request to your API sends the `Authorization: Bearer <token>` header. A JWT token is typically 300–500 bytes. If a page makes 50 API calls, that is 25 KB of repeated token data.

HTTP/2 uses HPACK compression. Headers are compressed and headers sent in previous requests are not repeated — only the changed headers are sent. This reduces bandwidth significantly for APIs with many requests.

**3. Server Push** *(brief introduction)*

The server can proactively send resources the client will need before it asks. For example, when sending the HTML, the server can push the main CSS file immediately, before the browser even parses the HTML and requests it. Used in practice but less common than expected — worth knowing the concept.

### G. HTTP/1.1 vs HTTP/2 Comparison

| Feature | HTTP/1.1 | HTTP/2 |
|---|---|---|
| Connections per host | Multiple (usually 6) | One |
| Request handling | Sequential per connection | Multiplexed (parallel) |
| Header format | Plain text, repeated every request | Binary, compressed (HPACK) |
| Head-of-line blocking | Yes (at application layer) | No (at application layer) |
| Server push | No | Yes |
| Encryption required | No (but HTTPS strongly recommended) | No (but all major browsers require TLS) |
| Adoption | Universal | Widely adopted (~65% of web traffic) |

### H. When it is used

- **When you enable it:** At the load balancer or reverse proxy layer. Nginx, Caddy, and AWS ALB support HTTP/2.
- **Between browser and server:** HTTP/2 is negotiated automatically using a TLS extension (ALPN). If both sides support it, it is used.
- **Between backend services:** Service-to-service calls often still use HTTP/1.1 because they make fewer concurrent requests and the benefit is smaller. gRPC (built on HTTP/2) is used when you need HTTP/2's benefits for internal traffic.

### I. Connection to system design

- **Fewer TCP connections** means fewer connection establishment costs and less load on the server's file descriptor limits.
- **Multiplexing** improves performance for frontend-heavy apps that make many small API calls.
- **HTTP/2 does not fix slow servers.** If your database query takes 300 ms, HTTP/2 does not help. It only improves the network transport layer.
- **HTTP/3** (built on QUIC over UDP) solves the remaining TCP-level head-of-line blocking in HTTP/2. Worth knowing exists; implementation details are for later.

### J. Common mistakes and misconceptions

**Misconception:** HTTP/2 requires changing my API or application code.
**Correction:** HTTP/2 is a transport-level change. Your HTTP routes, headers, status codes, and response bodies stay identical. You enable it at the infrastructure layer (Nginx, load balancer).

**Misconception:** HTTP/2 eliminates all head-of-line blocking.
**Correction:** HTTP/2 eliminates application-level head-of-line blocking. But since HTTP/2 still uses TCP, a single lost TCP packet blocks all streams until it is retransmitted. HTTP/3 on QUIC solves this by running each stream independently over UDP.

**Misconception:** HTTP/2 makes any website fast.
**Correction:** HTTP/2 reduces network overhead. Slow backend processing, large unoptimised images, and unminified JavaScript are not network problems — HTTP/2 does not help with them.

### K. Short interview answer

> "HTTP/1.1 processes one request at a time per TCP connection, which causes head-of-line blocking when a page loads many resources. Browsers work around this by opening multiple connections, but that adds handshake overhead. HTTP/2 introduces multiplexing — multiple requests and responses travel over one TCP connection simultaneously. It also compresses headers, which matters for APIs with many calls that repeat large headers like auth tokens. As a backend developer I enable HTTP/2 at the Nginx or load balancer layer — my application code does not change. It significantly improves performance for pages with many resources, especially on mobile networks with higher latency."

---

## 2. WebSockets

### A. Interview-ready definition

A **WebSocket** is a communication protocol that provides a persistent, full-duplex (two-way) channel over a single TCP connection between a client and a server. Unlike HTTP, where the client must always initiate a request to receive data, WebSockets allow the server to push data to the client at any time, making them suitable for real-time applications.

### B. Explanation in simple language

In HTTP, communication is always one-directional in each exchange: the client asks, the server answers. If you want live updates — like a chat message appearing instantly, a live score updating, or a stock price changing — you have a problem.

**The polling workaround (and why it is bad):**

Before WebSockets, developers used **polling**: the client asks the server "any new messages?" every 2 seconds.

```
Client: Any new messages?  → Server: No
Client: Any new messages?  → Server: No
Client: Any new messages?  → Server: No
Client: Any new messages?  → Server: YES — here is one
```

This wastes server resources (most requests get "No"), adds unnecessary load, and has up to a 2-second delay before the client sees a new message.

**WebSockets — one persistent connection:**

A WebSocket connection starts as an HTTP request, then upgrades to a WebSocket connection. After that, both sides can send data to the other at any time, without a new request.

```
Client ──────── HTTP Upgrade Request ──────────→ Server
Client ←─────── 101 Switching Protocols ────── Server
         ↕ Persistent bidirectional channel ↕
Client ←─────── "New order placed!" ─────────  Server (server pushes)
Client ──────── "Mark order as shipped" ──────→ Server (client sends)
Client ←─────── "Shipment confirmed" ───────── Server (server responds)
```

### C. Why it exists

HTTP was designed for request-response. It works perfectly for fetching resources. But for real-time use cases — chat, live notifications, collaborative editing, live dashboards — HTTP's model is the wrong tool. WebSockets exist to fill this gap: a persistent connection where both sides communicate freely.

### D. Real-life analogy

HTTP is like sending letters — you write a letter, send it, wait for a reply, write another letter. Each communication is a separate, complete exchange.

WebSockets are like a phone call — once connected, both parties speak and listen freely without hanging up and calling again for each sentence.

Where the analogy breaks down: WebSockets are still over TCP, so there is still underlying packet-level structure. But from the application's perspective, it behaves like a continuous open channel.

### E. Practical software example

ShopEasy adds a **live admin dashboard** that shows:
- New orders appearing in real time.
- Live inventory count updating as items are sold.
- Support chat between customers and agents.

**Without WebSockets (polling every 3 seconds):**
- 100 admins × 1 request per 3 seconds = 33 requests/second just to check for updates.
- Each request includes full HTTP headers (~500 bytes).
- Most requests return "no update."

**With WebSockets:**
- 100 admins each hold one persistent connection.
- Server pushes a message only when a new order arrives.
- Zero wasted requests.

### F. How WebSocket Connection Works

```mermaid
sequenceDiagram
    participant C as Client (Browser)
    participant S as Server

    C->>S: HTTP GET /ws\nUpgrade: websocket\nConnection: Upgrade
    S-->>C: HTTP 101 Switching Protocols\nUpgrade: websocket

    Note over C,S: TCP connection stays open — WebSocket channel active

    S-->>C: Push: {"event":"new_order","id":1042}
    C->>S: Send: {"action":"acknowledge","id":1042}
    S-->>C: Push: {"event":"inventory_update","item":"shoes","count":43}
    C->>S: Send: {"action":"ping"}
    S-->>C: {"action":"pong"}

    Note over C,S: Either side can close the connection
    C->>S: Close frame
    S-->>C: Close frame acknowledgement
```

**Key detail:** The WebSocket handshake is a standard HTTP request with special headers (`Upgrade: websocket`). The server responds with `101 Switching Protocols`. After this, the connection is no longer HTTP — it is a raw WebSocket frame stream over TCP.

### G. HTTP Request-Response vs WebSocket

| Aspect | HTTP Request-Response | WebSocket |
|---|---|---|
| Initiated by | Always the client | Either side |
| Direction | One request, one response | Full-duplex (both ways, any time) |
| Connection lifetime | Short — closes after response | Long-lived — stays open |
| Overhead per message | Full HTTP headers (~500 bytes) | Tiny frame header (~2–14 bytes) |
| Use case | Fetching data, submitting forms | Real-time: chat, live updates, gaming |
| Server push | No (client must ask) | Yes |

### H. When to use WebSockets

**Use WebSockets when:**
- The server needs to push data to clients without a client request.
- Low-latency bidirectional communication is needed.
- Many small messages are expected (polling overhead adds up).

**Examples:** Chat applications, live sports scores, collaborative editing (Google Docs-style), multiplayer games, live trading dashboards, real-time notifications.

**Do not use WebSockets when:**
- Simple request-response is enough (standard CRUD API).
- The server rarely sends unsolicited data.
- You need stateless, easily cacheable responses.
- You are building a simple REST API — WebSockets add complexity for no benefit.

**Alternative — Server-Sent Events (SSE):**
If you only need the server to push data to the client (not the other way), SSE is simpler than WebSockets — it is one-directional server-to-client streaming over HTTP. Use it for live notifications, live logs, or progress bars.

### I. Connection to system design

- **Statefulness:** A WebSocket connection is stateful — the server holds open connections for each connected client. If you have 100,000 users connected, the server holds 100,000 open connections. This affects memory and resource planning.
- **Horizontal scaling:** HTTP is stateless, so any server can handle any request. WebSockets are stateful — a client connected to Server A cannot receive a push from Server B unless you add a message broker (Redis Pub/Sub or Kafka) to relay messages between servers. This is a common system design question.
- **Load balancer configuration:** Load balancers must be configured for WebSocket support (sticky sessions or WebSocket-aware proxy). AWS ALB supports WebSockets natively.
- **Connection limits:** A single server can hold tens of thousands of WebSocket connections. Node.js's event-driven model handles this well.

### J. Common mistakes and misconceptions

**Misconception:** WebSockets are always better than HTTP for real-time.
**Correction:** For simple one-directional server-to-client updates (like a progress bar or live notification), SSE is simpler and works over standard HTTP. WebSockets are best when bidirectional communication is needed.

**Misconception:** WebSockets work everywhere HTTP/2 is used.
**Correction:** HTTP/2 has its own server push mechanism. WebSockets are separate and run on HTTP/1.1 by default in many implementations (though WebSockets over HTTP/2 is being standardised).

**Misconception:** WebSocket connections never drop.
**Correction:** Connections drop regularly — network changes, server restarts, idle timeouts. Production WebSocket implementations need reconnection logic, heartbeat pings to detect dead connections, and message queuing for reconnection.

### K. Short interview answer

> "WebSockets provide a persistent, full-duplex connection between client and server over a single TCP connection. The connection starts as an HTTP request with an Upgrade header, the server responds with 101 Switching Protocols, and from then on both sides can send messages freely without new requests. I use WebSockets when the server needs to push data to clients in real time — like chat messages, live order notifications, or a live dashboard. The key design consideration is that WebSocket connections are stateful, so horizontal scaling requires a message broker like Redis Pub/Sub to distribute messages across multiple server instances."

---

## 3. REST API Design

### A. Interview-ready definition

**REST (Representational State Transfer)** is an architectural style for designing networked APIs. A REST API uses standard HTTP methods to perform operations on **resources** identified by URLs. REST APIs are stateless — each request contains all the information needed to process it, and the server stores no client session state between requests.

### B. Explanation in simple language

REST is not a protocol or a library — it is a set of design principles for building APIs that are consistent, predictable, and easy to use.

The core idea: **everything is a resource** (a user, an order, a product), and you perform actions on those resources using HTTP methods.

**Bad API design (non-REST):**
```
POST /getUser
POST /createNewOrder
POST /deleteProductById
POST /updateUserEmail
```
Everything is a POST. The action is in the URL. There is no consistency.

**REST API design:**
```
GET    /users/42          → get user with ID 42
POST   /users             → create a new user
PUT    /users/42          → replace user 42 completely
PATCH  /users/42          → update part of user 42 (e.g., only email)
DELETE /users/42          → delete user 42
```
The HTTP method tells you **what** is happening. The URL tells you **what resource** is affected.

### C. REST Design Principles You Must Know

**1. Resources are nouns, not verbs**

```
GET /orders          (noun — the resource)
❌ GET /getOrders       (verb in URL — not RESTful)

POST /products       (create a product)
❌ POST /createProduct  (redundant verb)
```

**2. Use plural nouns for collections**

```
/users       (collection)
/users/42    (one item in the collection)
❌ /user        (singular — inconsistent)
```

**3. Use nested resources for relationships**

```
GET  /users/42/orders        → all orders belonging to user 42
GET  /users/42/orders/7      → order 7 belonging to user 42
POST /users/42/orders        → create an order for user 42
```

Only nest one level deep. Deeply nested URLs (`/users/42/orders/7/items/3/reviews`) become unmanageable.

**4. Use query parameters for filtering, sorting, and pagination**

```
GET /products?category=shoes&sort=price&order=asc&page=2&limit=20
```

Do not put filters in the path. The path identifies the resource. Query parameters modify how the collection is returned.

**5. Return the right HTTP status code**

```
POST   /orders    → 201 Created  (not 200)
DELETE /orders/5  → 204 No Content (no body needed)
GET    /orders/99 → 404 Not Found (if 99 does not exist)
POST   /orders    → 400 Bad Request (if required fields are missing)
```

**6. Version your API**

```
/api/v1/products
/api/v2/products
```

Versioning lets you make breaking changes without breaking existing clients. Put the version in the URL or in a header (URL versioning is more common and visible).

### D. Practical software example — ShopEasy API

```
# Products
GET    /api/v1/products                   List all products (paginated)
GET    /api/v1/products?category=shoes    Filter products
GET    /api/v1/products/101               Get one product
POST   /api/v1/products                   Create a product (admin only)
PUT    /api/v1/products/101               Replace product 101
PATCH  /api/v1/products/101               Update product 101 partially
DELETE /api/v1/products/101               Delete product 101

# Orders (nested under users)
GET    /api/v1/users/42/orders            All orders for user 42
POST   /api/v1/users/42/orders            Place a new order for user 42
GET    /api/v1/users/42/orders/7          Specific order
PATCH  /api/v1/users/42/orders/7          Update order status
```

**What to include in every response:**
```json
{
  "data": { "id": 101, "name": "Running Shoes", "price": 2999 },
  "meta": { "request_id": "abc-123", "timestamp": "2026-10-07T08:00:00Z" }
}
```

**Error response (consistent format):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "price must be a positive number",
    "field": "price"
  }
}
```

### E. Statelessness — Why it matters for scaling

A REST API is **stateless** — the server does not remember anything about a client between requests. Every request must carry all information the server needs (authentication token, parameters, body).

**Why this matters:**

```
Request 1 → Server A (handles it)
Request 2 → Server B (handles it, no problem)
Request 3 → Server C (handles it, no problem)
```

Because the server has no session state, any server in a load-balanced pool can handle any request. This is what makes REST APIs horizontally scalable — add more servers, distribute requests freely.

If the server stored session state, Request 2 would need to go to the same server that handled Request 1, limiting your ability to scale.

### F. Common mistakes and misconceptions

**Misconception:** REST is a specification with strict rules.
**Correction:** REST is an architectural style with principles, not a strict standard. You can follow it loosely or strictly. What matters is that your API is consistent and predictable for consumers.

**Misconception:** REST is the only way to build APIs.
**Correction:** GraphQL, gRPC, and tRPC are popular alternatives. REST is the most common and is the right default for most web APIs. GraphQL is better when clients need flexible queries over complex data graphs.

**Misconception:** PUT and PATCH are the same thing.
**Correction:** PUT replaces the entire resource. If you PUT `{"name":"Shoes"}` on a product that also has a `price` field, the `price` is gone. PATCH updates only the fields you send. In practice, most APIs implement PATCH behaviour and call it PUT — but in interviews, state the distinction correctly.

### G. Short interview answer

> "REST is an architectural style where resources are identified by URLs and operations are performed using standard HTTP methods — GET to read, POST to create, PUT or PATCH to update, DELETE to remove. The key principles I follow are: use plural nouns in paths, not verbs; use HTTP methods to express intent; use the correct status code in responses; use query parameters for filtering and pagination; and keep the API stateless so any server instance can handle any request. Statelessness is what makes REST APIs easy to scale horizontally behind a load balancer."

---

## 4. CORS — Cross-Origin Resource Sharing

### A. Interview-ready definition

**CORS (Cross-Origin Resource Sharing)** is a browser security mechanism that controls whether a web page running at one origin (domain + scheme + port) is allowed to make HTTP requests to a different origin. By default, browsers block such cross-origin requests unless the target server explicitly permits them using specific HTTP response headers.

### B. Explanation in simple language

**What is an "origin"?**

An origin is the combination of three things:
- **Scheme:** `http` or `https`
- **Domain:** `shopeasy.com`
- **Port:** `443`

Two URLs have the same origin only if all three match exactly.

```
https://shopeasy.com           (origin A)
https://api.shopeasy.com       (different origin — different subdomain)
http://shopeasy.com            (different origin — different scheme)
https://shopeasy.com:8080      (different origin — different port)
```

**The Same-Origin Policy:**

Browsers enforce the **Same-Origin Policy**: JavaScript running on `https://shopeasy.com` cannot make requests to `https://api.shopeasy.com` by default. This protects users — without it, a malicious website could make requests to your bank's API using your browser's stored cookies.

**CORS: The controlled exception:**

CORS lets a server declare: "I allow requests from this specific other origin." The browser checks the server's permission headers and either allows or blocks the request.

### C. Why it exists

Imagine you are logged into `bank.com`. A malicious website at `evil.com` runs JavaScript that makes a request to `bank.com/transfer?to=attacker&amount=50000`. Without the Same-Origin Policy, the browser would send your `bank.com` session cookie with that request, and the transfer would succeed.

The Same-Origin Policy prevents this. CORS then provides a controlled way for legitimate cross-origin communication (your React frontend at `shopeasy.com` talking to your API at `api.shopeasy.com`).

### D. Real-life analogy

Think of CORS as a nightclub's guest list policy. By default, the club (your API server) only lets in people from its own building (same origin). If you want to let in guests from another building (your frontend on a different domain), you add them to the guest list. The bouncer (the browser) checks the list before letting anyone in.

The key: the bouncer is your browser, not your server. The server just provides the guest list in its headers.

### E. How CORS Works — Step by Step

**Simple request (GET or POST with standard headers):**

```mermaid
sequenceDiagram
    participant B as Browser (shopeasy.com)
    participant S as API Server (api.shopeasy.com)

    B->>S: GET /products\nOrigin: https://shopeasy.com
    S-->>B: 200 OK\nAccess-Control-Allow-Origin: https://shopeasy.com
    Note over B: Origin matches → browser allows JS to read response
```

**Preflight request (for non-simple requests: PUT, DELETE, custom headers):**

For requests that might have side effects, the browser first sends an **OPTIONS** preflight request to ask for permission before the actual request.

```mermaid
sequenceDiagram
    participant B as Browser (shopeasy.com)
    participant S as API Server (api.shopeasy.com)

    B->>S: OPTIONS /orders\nOrigin: https://shopeasy.com\nAccess-Control-Request-Method: DELETE\nAccess-Control-Request-Headers: Authorization

    S-->>B: 204 No Content\nAccess-Control-Allow-Origin: https://shopeasy.com\nAccess-Control-Allow-Methods: GET, POST, PUT, DELETE\nAccess-Control-Allow-Headers: Authorization, Content-Type\nAccess-Control-Max-Age: 86400

    Note over B: Preflight approved — send actual request
    B->>S: DELETE /orders/7\nOrigin: https://shopeasy.com\nAuthorization: Bearer eyJ...

    S-->>B: 204 No Content
```

**`Access-Control-Max-Age: 86400`** means the browser caches this preflight result for 86400 seconds (1 day), avoiding the preflight on every subsequent request.

### F. Important CORS Headers

| Header | Direction | Purpose |
|---|---|---|
| `Origin` | Request | Browser sends the origin of the requesting page |
| `Access-Control-Allow-Origin` | Response | Which origins are permitted (`*` or a specific origin) |
| `Access-Control-Allow-Methods` | Response (preflight) | Which HTTP methods are permitted |
| `Access-Control-Allow-Headers` | Response (preflight) | Which request headers are permitted |
| `Access-Control-Allow-Credentials` | Response | Whether cookies/auth can be included |
| `Access-Control-Max-Age` | Response (preflight) | How long the browser can cache this preflight |

**Critical detail — `Access-Control-Allow-Origin: *` and credentials:**

You cannot use `Access-Control-Allow-Origin: *` (allow all origins) together with `Access-Control-Allow-Credentials: true`. If you need to send cookies or auth headers cross-origin, you must specify the exact origin.

```
# This combination does not work:
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true    ← Browser will block this

# This works:
Access-Control-Allow-Origin: https://shopeasy.com
Access-Control-Allow-Credentials: true
```

### G. CORS is a browser restriction — not a server restriction

**This is the most important thing to understand about CORS:**

CORS is enforced by the browser. It protects users. A server cannot enforce CORS on requests from non-browser clients.

```
curl https://api.shopeasy.com/products    ← No CORS enforcement. Works.
Postman → https://api.shopeasy.com/products  ← No CORS enforcement. Works.
Browser JS → https://api.shopeasy.com/products  ← CORS enforced. Blocked if headers missing.
```

This is why you can test your API in Postman without CORS issues, but it fails in the browser. CORS is not a security mechanism for your API — it is a user-protection mechanism in browsers.

Your API security comes from authentication and authorisation, not CORS.

### H. Common mistakes and misconceptions

**Misconception:** CORS is a server-side security feature that protects my API.
**Correction:** CORS protects the user's browser from malicious cross-site requests. It is enforced by the browser, not the server. Non-browser clients (curl, Postman, other servers) bypass CORS completely. Authenticate and authorise every API request regardless of CORS settings.

**Misconception:** `Access-Control-Allow-Origin: *` means my API is open to the internet.
**Correction:** This header tells browsers it is safe to read responses from any origin. It does not affect who can make requests — anyone can make requests to your API from any tool. You still need authentication.

**Misconception:** CORS errors are a backend bug.
**Correction:** CORS errors occur when the server's response headers do not permit the browser's origin. The fix is on the server (add the correct CORS headers). But the reason CORS exists is a browser security feature — neither side is "buggy."

**Misconception:** Preflights happen for every request.
**Correction:** Browsers send a preflight only for non-simple requests (non-GET/POST, or requests with custom headers like `Authorization`). Simple GET requests do not trigger a preflight. Preflights are also cached using `Access-Control-Max-Age`.

### I. Short interview answer

> "CORS stands for Cross-Origin Resource Sharing. By default, browsers block JavaScript from making requests to a different origin — a different domain, scheme, or port — to protect users from cross-site request attacks. CORS lets a server declare which origins it permits by returning Access-Control-Allow-Origin and related headers. For non-simple requests like DELETE or anything with an Authorization header, the browser first sends an OPTIONS preflight request asking for permission. The critical thing to understand is that CORS is enforced by the browser, not the server — curl and Postman bypass it. So CORS is not API security; it's user protection. API security comes from authentication."

---

## 5. Authentication: JWT vs Sessions

### A. Interview-ready definition

**Session-based authentication** stores authentication state on the server. When a user logs in, the server creates a session record and sends a session ID to the client in a cookie. On each subsequent request, the client sends the cookie, and the server looks up the session. **JWT (JSON Web Token) authentication** stores authentication state in a signed token on the client. The server verifies the token's signature on each request without storing any session data.

### B. Explanation in simple language

After a user logs in, the server needs a way to identify them on every subsequent request. There are two main approaches.

**Session-based authentication:**

Think of a coat check at a venue. You hand in your coat (credentials), they give you a numbered ticket (session ID). When you want your coat back, you show the ticket. They look up the number in their records and retrieve your coat.

```
1. User logs in with email + password
2. Server verifies credentials
3. Server creates a session: { id: "abc123", userId: 42, role: "admin" }
4. Session is stored in server memory or Redis
5. Server sends cookie: Set-Cookie: session_id=abc123; HttpOnly; Secure
6. Browser stores cookie and sends it automatically on every request
7. Server receives request → looks up "abc123" in session store → finds user 42
```

**JWT authentication:**

Think of a driving licence. It contains your information (name, date of birth) and is digitally signed by the government. Any authority can verify it by checking the signature — they do not need to call the government's database. The licence holder carries it, not the government.

```
1. User logs in with email + password
2. Server verifies credentials
3. Server creates a JWT: { userId: 42, role: "admin", exp: 1728000000 }
   and signs it with a secret key
4. Server sends JWT to client (usually in response body)
5. Client stores it (localStorage or memory) and sends it in every request header:
   Authorization: Bearer eyJhbGc...
6. Server receives request → verifies JWT signature → reads user info from token
   → no database lookup needed
```

### C. JWT Structure

A JWT has three parts separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjQyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
     HEADER                   PAYLOAD                    SIGNATURE
```

**Header:** Algorithm used to sign (`HS256`, `RS256`)
**Payload:** The data — called **claims** — in base64-encoded JSON:
```json
{
  "userId": 42,
  "role": "admin",
  "exp": 1728000000,
  "iat": 1727913600
}
```
**Signature:** `HMACSHA256(base64(header) + "." + base64(payload), secretKey)`

The server verifies by recomputing the signature and comparing. If it matches, the token is valid and was not tampered with.

> **Important:** The payload is only base64-encoded, not encrypted. Anyone who has the token can decode and read the payload. Never put passwords, card numbers, or sensitive data in a JWT payload.

### D. Session vs JWT Comparison

| Aspect | Session | JWT |
|---|---|---|
| State stored on | Server (memory or Redis) | Client (the token itself) |
| Server lookup per request | Yes — query session store | No — verify signature only |
| Revocation | Easy — delete session from store | Hard — cannot invalidate without a blocklist |
| Horizontal scaling | Requires shared session store (Redis) | Stateless — any server can verify |
| Token size | Small (just a session ID, e.g. 32 bytes) | Larger (typically 300–600 bytes in headers) |
| Best for | Traditional web apps with server-side rendering | SPAs, mobile apps, microservices |

### E. The JWT Revocation Problem — and how to solve it

This is a common interview question.

**The problem:** A JWT is valid until it expires. If a user's account is compromised, or a user logs out, how do you invalidate their JWT before it expires?

You cannot. The server has no state, so there is nothing to delete.

**Solutions:**

1. **Short expiry times:** Set JWT expiry to 15 minutes. Pair it with a **refresh token** (a long-lived, stored token used only to get a new JWT).

```
Access token:  expires in 15 minutes (stored in memory, short-lived)
Refresh token: expires in 30 days (stored HttpOnly cookie, long-lived)
```

When the access token expires, the client sends the refresh token to get a new access token. When a user logs out, the server invalidates the refresh token (stored in DB). The old access token expires in ≤ 15 minutes.

2. **JWT blocklist:** Store invalidated token IDs in Redis. Check every JWT against this blocklist. This adds a Redis lookup per request — you lose the stateless benefit, but gain instant revocation.

### F. When to use which

**Use sessions when:**
- Traditional server-rendered web application.
- You need instant, reliable revocation (banking, healthcare).
- All requests go through a single backend or a backend with a shared Redis.

**Use JWT when:**
- Single-page application or mobile app.
- Multiple services need to verify identity without calling a central auth server.
- You are building a microservices system where services validate tokens independently.

### G. Security considerations

| Practice | Why |
|---|---|
| Use `HttpOnly` cookie for refresh tokens | JavaScript cannot steal it (XSS protection) |
| Use `Secure` flag | Cookie only sent over HTTPS |
| Set short expiry on access tokens (15 min) | Limit damage if token is stolen |
| Never store access JWT in localStorage | Vulnerable to XSS attacks |
| Always verify JWT signature on every request | Never trust the payload without signature verification |
| Never put sensitive data in JWT payload | Payload is readable by anyone |

### H. Common mistakes and misconceptions

**Misconception:** JWT is always more secure than sessions.
**Correction:** Neither is universally more secure. Sessions offer easier revocation. JWTs offer stateless scalability. Security depends on implementation, not the mechanism.

**Misconception:** JWT payload is encrypted.
**Correction:** The payload is base64-encoded, not encrypted. It is readable by anyone who has the token. Use JWE (JSON Web Encryption) if you need to encrypt the payload — but this is uncommon.

**Misconception:** Logging out invalidates a JWT.
**Correction:** JWT logout on the client means deleting the token from client storage. The token itself remains valid until expiry. This is why short expiry times and refresh tokens are the correct pattern.

### I. Short interview answer

> "Session-based auth stores state on the server: after login, the server creates a session, stores it in Redis, and sends a session ID cookie to the client. Every request requires a session store lookup. JWT auth is stateless: the server signs a token containing user info and sends it to the client. On each request, the server just verifies the signature — no database lookup. JWT scales better horizontally because any server can verify the token. The key trade-off is revocation: sessions are easy to revoke by deleting from the store. JWTs cannot be invalidated before expiry, so I use short-lived access tokens (15 minutes) paired with long-lived refresh tokens. The refresh token is stored in an HttpOnly cookie and can be revoked server-side."

---

## 6. HTTP Caching and Cache-Control

### A. Interview-ready definition

**HTTP caching** is a mechanism that stores copies of HTTP responses so that future requests for the same resource can be served from the cache rather than the origin server. The `Cache-Control` header lets the server specify caching rules: how long a response can be cached, who can cache it, and under what conditions it must be revalidated.

### B. Explanation in simple language

Every time a user loads a product image on ShopEasy, should your server generate and send the same 200 KB image file again? No — once a browser downloads it, it can store it locally and reuse it for the next hour, day, or week.

HTTP caching sits at multiple levels:
- **Browser cache:** The user's browser stores responses locally.
- **CDN cache:** A CDN server between the user and your origin stores responses closer to the user.
- **Reverse proxy cache:** An Nginx or Varnish cache in front of your servers.

Caching reduces server load, reduces bandwidth costs, and dramatically reduces latency for repeat visitors.

### C. Cache-Control Header — The Key Directives

The `Cache-Control` header is returned by the server and tells caches how to behave.

| Directive | Meaning |
|---|---|
| `max-age=3600` | Cache this response for 3600 seconds (1 hour) |
| `no-cache` | Cache is allowed, but must revalidate with server before using it |
| `no-store` | Do not cache at all — sensitive data (bank statements, OTPs) |
| `public` | Any cache (browser, CDN) can store this |
| `private` | Only the end-user's browser can cache this (not CDN) |
| `must-revalidate` | Once expired, must revalidate before using stale copy |
| `s-maxage=86400` | CDN-specific max-age (overrides `max-age` for shared caches) |

### D. Practical examples for ShopEasy

```
# Product images — change rarely, can be cached by CDN for 7 days
Cache-Control: public, max-age=604800

# User profile data — private, browser only, revalidate after 5 minutes
Cache-Control: private, max-age=300

# Order confirmation page — do not cache at all
Cache-Control: no-store

# Home page — CDNs can cache for 1 hour, revalidate after
Cache-Control: public, s-maxage=3600, must-revalidate

# API response for product list — CDN cache for 60 seconds
Cache-Control: public, s-maxage=60
```

### E. ETag and Conditional Requests (Revalidation)

When a cached response expires, the browser does not necessarily download the full resource again. It can ask the server: "Has this changed since I last fetched it?"

**ETag** (Entity Tag) is a unique identifier (like a hash) for a specific version of a resource.

```
First request:
  GET /products/101
  ← 200 OK
     ETag: "abc123"
     Cache-Control: max-age=60
     [full product data]

After 60 seconds (cache expired):
  GET /products/101
  If-None-Match: "abc123"   (browser sends the old ETag)

  ← 304 Not Modified        (if unchanged — no body, tiny response!)
    or
  ← 200 OK + new ETag       (if changed — full new response)
```

A **304 Not Modified** response has no body — just headers. This saves bandwidth and is faster than resending the full resource.

### F. Caching Decision Diagram

```mermaid
flowchart TD
    A["Request for /products/101"] --> B{"Browser cache\nhit?"}
    B -->|"Yes, not expired"| C["Serve from browser cache\n0ms latency"]
    B -->|"No or expired"| D{"CDN cache\nhit?"}
    D -->|"Yes, not expired"| E["Serve from CDN\nLow latency"]
    D -->|"No or expired"| F["Origin server"]
    F --> G["Query database"]
    G --> H["Return response\nwith Cache-Control headers"]
    H --> I["CDN caches response"]
    I --> J["Browser caches response"]
```

### G. What to cache and what not to cache

| Resource | Cache? | Why |
|---|---|---|
| Product images | Yes, aggressively (days/weeks) | Rarely change, large files |
| Static JS/CSS | Yes, with versioned filenames | Bundle hash changes on deploy |
| Product listings | Yes, short TTL (60–300 s) | Changes occasionally |
| User profile | Browser only, short TTL | Private data |
| Authentication tokens | Never | Security |
| OTP pages | Never | Sensitive, one-time |
| Order confirmation | Never | Unique, sensitive |

**Cache-busting for static files:**

When you deploy a new version of your CSS file, you need users to download the new version, not use the cached old one. The solution: include a hash in the filename.

```
style.abc123.css   ← current version (cached for 1 year)
style.def456.css   ← new version after deploy (new URL, browser fetches fresh)
```

Because the URL changed, the browser has no cached version and downloads the new file. This lets you set `max-age` to 1 year for static assets safely.

### H. Connection to system design

- **CDN + Cache-Control:** Setting appropriate `s-maxage` headers lets your CDN absorb most traffic for popular content, dramatically reducing origin server load.
- **Database load reduction:** Caching API responses (even for 60 seconds) can reduce database queries by orders of magnitude during traffic spikes.
- **Cache invalidation:** "There are only two hard things in computer science: cache invalidation and naming things." When data changes, how do you clear the relevant cached responses? This is a real design challenge — worth discussing in interviews.

### I. Common mistakes and misconceptions

**Misconception:** `no-cache` means "do not cache."
**Correction:** `no-cache` means "you may cache, but you must validate with the server before using the cached copy." Use `no-store` if you truly do not want caching.

**Misconception:** Caching is only for static files.
**Correction:** API responses can and should be cached when appropriate. A product list that changes every few minutes can be cached with a 60-second TTL. This is often the difference between a server handling 100 requests/second and 10,000 requests/second.

### J. Short interview answer

> "HTTP caching lets browsers and CDNs store response copies to avoid fetching the same resource from the origin server repeatedly. The Cache-Control header controls this: max-age sets how long the cache is valid, public allows CDNs to cache it, private restricts it to the browser only, and no-store disables caching entirely for sensitive data. I use aggressive caching for static assets using content-hashed filenames so I can set a year-long max-age safely. For API responses, short TTLs like 60 seconds can dramatically reduce database load during traffic spikes. ETags let clients revalidate expired caches cheaply — a 304 Not Modified response has no body, saving bandwidth."

---

## 7. Service-to-Service Communication

### A. Interview-ready definition

**Service-to-service communication** refers to how backend services (microservices or monolith components) call each other over a network. This can be **synchronous** — the caller waits for an immediate response (using HTTP or gRPC) — or **asynchronous** — the caller sends a message and continues without waiting for a response (using message queues like Kafka or RabbitMQ).

### B. Explanation in simple language

A modern backend system rarely has one service. ShopEasy might have:
- An **Order Service** that handles order placement.
- An **Inventory Service** that tracks product stock.
- A **Notification Service** that sends emails and SMS.
- A **Payment Service** that processes charges.

When a user places an order, the Order Service needs to:
1. Check if the item is in stock (Inventory Service).
2. Charge the user (Payment Service).
3. Send a confirmation email (Notification Service).

How these services communicate affects reliability, latency, and scalability.

### C. Synchronous Communication (HTTP REST)

The Order Service calls the Inventory Service and waits for a response before continuing.

```mermaid
sequenceDiagram
    participant O as Order Service
    participant I as Inventory Service
    participant P as Payment Service
    participant N as Notification Service

    O->>I: GET /inventory/shoes-42 (is it in stock?)
    I-->>O: 200 OK {"stock": 15}
    O->>P: POST /charge {"amount": 2999, "userId": 42}
    P-->>O: 200 OK {"transactionId": "txn_abc"}
    O->>N: POST /notify {"userId": 42, "type": "order_confirmed"}
    N-->>O: 200 OK
    O-->>Client: 201 Order created
```

**Total latency = sum of all service calls.** If each takes 50 ms, the user waits at least 150 ms just for service communication.

**Risk:** If any service is slow or down, the Order Service fails or times out. This is called **tight coupling**.

### D. Asynchronous Communication (Message Queue)

For operations that do not need to happen before responding to the user, use async:

```mermaid
sequenceDiagram
    participant O as Order Service
    participant I as Inventory Service
    participant Q as Message Queue (Kafka/RabbitMQ)
    participant N as Notification Service

    O->>I: Check stock (sync — user is waiting)
    I-->>O: In stock
    O->>Q: Publish "order.created" event
    O-->>Client: 201 Order created (immediate response!)

    Note over Q,N: Async — user has already received response
    Q->>N: Deliver "order.created" event
    N->>N: Send confirmation email
```

The user gets an immediate response. The email is sent asynchronously in the background. Even if the Notification Service is temporarily down, the message stays in the queue and is delivered when it recovers.

### E. Synchronous vs Asynchronous Communication

| Aspect | Synchronous (HTTP) | Asynchronous (Queue) |
|---|---|---|
| Caller behaviour | Waits for response | Sends message and continues |
| Latency impact | Adds directly to response time | Does not block response |
| Failure handling | Caller fails if service is down | Messages queue up if service is down |
| Coupling | Tight (caller needs receiver up) | Loose (decoupled by queue) |
| Complexity | Simple | Higher (queue infrastructure needed) |
| Use when | Need immediate result | Operations can happen after response |

### F. Connection Pooling — Essential for Backend Services

Every time your backend connects to a database, a new TCP connection costs a handshake. In a high-traffic API:

- 1,000 requests/second × 1 new connection each = 1,000 TCP handshakes/second.
- At 5 ms per handshake = 5 seconds of connection overhead per second.

**Connection pooling** maintains a pool of pre-established connections. Each request borrows a connection, uses it, and returns it to the pool.

```
Pool: [conn1] [conn2] [conn3] [conn4] [conn5]   ← all pre-established

Request A → borrows conn1 → queries → returns conn1
Request B → borrows conn2 → queries → returns conn2
Request C → borrows conn3 → queries → returns conn3
```

**Key settings to know:**
- **Pool size:** How many connections to maintain. Too small → requests queue. Too large → database runs out of connection slots.
- **Timeout:** How long to wait for a connection from the pool before erroring.
- **Max lifetime:** Connections are periodically replaced to avoid stale TCP connections dropped by firewalls.

Most ORMs and database clients handle this automatically — but you need to configure the pool size correctly for your traffic.

### G. Timeouts — Always Set Them

Every service-to-service call must have a timeout. Without one:

```
Order Service → calls Payment Service (which is slow)
Payment Service takes 30 seconds to respond
Order Service thread is blocked for 30 seconds, holding a connection
1000 simultaneous slow payment calls = 1000 blocked Order Service threads
Order Service runs out of threads → completely unresponsive → cascade failure
```

With a 3-second timeout:

```
After 3 seconds → timeout → Order Service returns 504 to client
Order Service is still responsive to other requests
Only users trying to pay are affected
```

**Circuit breaker pattern** (brief introduction): If a downstream service fails consistently, a circuit breaker stops sending requests to it for a period, returning errors immediately rather than waiting for timeouts. This prevents cascade failures. (Hystrix, Resilience4j implement this.)

### H. Common mistakes and misconceptions

**Misconception:** Microservices always communicate via REST HTTP.
**Correction:** Many microservice systems use gRPC for internal service communication (more efficient than REST for high-frequency calls), or message queues for async operations. REST is one option, not the only one.

**Misconception:** Setting a very high timeout is safe.
**Correction:** High timeouts allow slow services to block caller threads for longer, increasing cascade failure risk. Timeouts should be set to slightly above the realistic SLA of the downstream service.

**Misconception:** Connection pooling is automatic and requires no configuration.
**Correction:** Most clients create a default pool, but the default size is often too small for high-traffic production systems. You need to configure pool size based on your request rate and database capacity.

### I. Short interview answer

> "Service-to-service communication is either synchronous or asynchronous. For operations that need an immediate response — like checking inventory before confirming an order — I use synchronous HTTP calls. The risk is tight coupling: if any service is slow, the caller is slow too, so I set strict timeouts on every outbound call. For operations that can happen after responding to the user — like sending a confirmation email — I use async communication through a message queue. The message is published and the caller responds immediately; the consumer processes it independently. For database connections, I always configure a connection pool so we reuse established TCP connections rather than creating new ones for every request."

---

## 8. Practical Exercises

### Exercise 1 — Observe HTTP/2 in Browser DevTools

**Purpose:** See HTTP/2 multiplexing in action.

**Steps:**
1. Open Chrome → `F12` → **Network** tab.
2. Visit `https://www.youtube.com`.
3. Right-click on the column headers in the Network tab → enable **Protocol**.
4. Look at the Protocol column.

**What to observe:**
- Most resources show `h2` — this is HTTP/2.
- Notice that many resources load simultaneously over a small number of connections.
- Older resources or third-party domains may still show `http/1.1`.

**What it does not prove:** You cannot directly see the multiplexing within a single connection in DevTools, but the low connection count and parallel loading is evidence of it.

**Interview connection:** "I check the Protocol column in DevTools to verify HTTP/2 is active. If I see http/1.1 for everything, it usually means HTTP/2 is not configured on the load balancer or Nginx."

---

### Exercise 2 — Trigger and inspect a CORS error

**Purpose:** See a real CORS error and understand the browser's enforcement.

**Steps:**
1. Open Chrome → `F12` → **Console** tab.
2. Go to `https://google.com` (so your origin is `https://google.com`).
3. In the console, type:
```javascript
fetch('https://api.github.com/users/octocat')
  .then(r => r.json())
  .then(console.log)
```
4. This works (GitHub allows all origins).

5. Now try a server that has CORS blocked:
```javascript
fetch('https://httpbin.org/get', {
  headers: { 'X-Custom-Header': 'test' }
})
```
6. Check the **Network** tab → look for the OPTIONS preflight request.

**What to observe:**
- The preflight OPTIONS request before the actual request.
- The `Access-Control-Allow-*` headers in the preflight response.
- How the browser either allows or blocks the subsequent request.

**Interview connection:** "When a developer sees a CORS error in the browser, the fix is always on the server — add the correct Access-Control-Allow-Origin header. The browser is correctly enforcing the server's policy."

---

### Exercise 3 — Decode a JWT

**Purpose:** Understand that JWTs are readable, not encrypted.

**Steps:**
1. Go to [https://jwt.io](https://jwt.io) in your browser.
2. The site shows a sample JWT. Look at the decoded payload on the right.
3. Change a value in the payload — notice the signature becomes invalid (shown in red).
4. If you have a JWT from a personal project (not production!), paste it and see its contents.

**What to observe:**
- The payload is human-readable JSON — just base64-encoded.
- Changing any part of the payload breaks the signature.
- The algorithm is shown in the header.

**What it does not prove:** This shows the JWT structure. It does not show the server-side verification logic.

**Interview connection:** "JWT payloads are base64-encoded, not encrypted. Anyone with the token can decode and read the claims. That's why I never put sensitive information like passwords or card numbers in the payload."

---

### Exercise 4 — Inspect Cache-Control headers

**Purpose:** See caching in action on a real site.

**Steps:**
1. Open Chrome → `F12` → **Network** tab.
2. Visit `https://github.com`.
3. Click on a `.js` or `.css` resource in the Network tab.
4. Look at the **Response Headers** section.

**What to observe:**
- `cache-control: max-age=31536000` on static assets (1 year).
- `etag: "abc123"` — the version identifier.
- Reload the page — notice some resources are served `(from disk cache)` — zero time.

**What it does not prove:** You see the declared caching rules. You cannot see whether a CDN cache served the response (CDN caches are transparent to DevTools).

**Interview connection:** "I set long max-age on static assets because we use content hashes in filenames. When we deploy, the filename changes, so browsers fetch the new file. Short TTLs on API responses balance freshness with server load."

---

### Exercise 5 — See active connections with netstat

**Purpose:** See real TCP connections your machine holds.

**Command (Windows PowerShell):**
```powershell
netstat -ano | findstr ESTABLISHED
```

**What to observe:**
- Each line is an active TCP connection: local IP:port → remote IP:port.
- You will see connections to servers for any open browser tabs, apps running in the background.
- The PID (last column) lets you identify which application owns the connection.

To find the application:
```powershell
tasklist | findstr <PID>
```

**What it does not prove:** `netstat` shows TCP connections. It does not show UDP or HTTP/2 streams.

**Interview connection:** "When debugging connection exhaustion issues, I use netstat to see how many connections a process holds and whether they are in ESTABLISHED, TIME_WAIT, or CLOSE_WAIT state. Too many TIME_WAIT connections often indicates connection pooling is not configured."

---

## 9. Quick Reference Tables

### HTTP/1.1 vs HTTP/2

| Feature | HTTP/1.1 | HTTP/2 |
|---|---|---|
| Connections | Many (6 per host) | One |
| Request handling | Sequential per connection | Multiplexed |
| Headers | Plain text, repeated | Binary, compressed |
| Server push | No | Yes |

### Session vs JWT

| Aspect | Session | JWT |
|---|---|---|
| State location | Server | Client (token) |
| Server lookup | Yes (Redis/DB) | No (verify signature) |
| Revocation | Easy | Hard (needs blocklist or short expiry) |
| Horizontal scaling | Shared store needed | Stateless |

### Sync vs Async Service Communication

| Aspect | Synchronous (HTTP) | Asynchronous (Queue) |
|---|---|---|
| Caller blocks | Yes | No |
| Downstream outage | Caller fails | Messages queue up |
| Coupling | Tight | Loose |
| Use case | Need immediate result | Background operations |

### HTTP Caching Directives

| Directive | Meaning |
|---|---|
| `max-age=N` | Cache valid for N seconds |
| `public` | CDN and browser can cache |
| `private` | Browser only |
| `no-cache` | Cache allowed, must revalidate |
| `no-store` | Never cache |
| `s-maxage=N` | CDN-specific TTL |

### CORS Key Headers

| Header | Direction | Purpose |
|---|---|---|
| `Origin` | Request | Browser's origin |
| `Access-Control-Allow-Origin` | Response | Permitted origins |
| `Access-Control-Allow-Methods` | Response (preflight) | Permitted methods |
| `Access-Control-Allow-Headers` | Response (preflight) | Permitted headers |
| `Access-Control-Max-Age` | Response (preflight) | Cache duration |

---

## 10. Final Interview Prep

### 12 Questions You Must Be Able to Answer Confidently

**Q1: What problem does HTTP/2 solve over HTTP/1.1?**
> HTTP/1.1 can only process one request at a time per TCP connection, causing head-of-line blocking when a page loads many resources. HTTP/2 solves this with multiplexing — multiple requests and responses travel simultaneously over one connection. It also compresses headers. As a backend developer I enable this at the Nginx or load balancer level without changing application code.

**Q2: When would you use WebSockets instead of HTTP?**
> When the server needs to push data to the client without the client asking, or when low-latency bidirectional communication is needed. Examples are chat, live notifications, and real-time dashboards. For simple request-response APIs, HTTP is simpler and the right choice. The key design consideration with WebSockets is that connections are stateful, so horizontal scaling requires a shared message broker like Redis Pub/Sub.

**Q3: What is CORS and why does it exist?**
> CORS is a browser security mechanism that controls which origins a web page can make HTTP requests to. It exists because the browser's Same-Origin Policy prevents cross-origin requests by default, protecting users from cross-site request forgery. The server declares permitted origins using Access-Control-Allow-Origin headers. CORS is enforced by the browser, not the server — non-browser clients bypass it entirely.

**Q4: What is a CORS preflight request?**
> For non-simple requests — PUT, DELETE, or requests with custom headers like Authorization — the browser first sends an OPTIONS preflight to ask the server for permission before sending the real request. The server responds with the allowed methods, headers, and origins. The browser caches this preflight using the Access-Control-Max-Age header to avoid repeating it on every request.

**Q5: What is the difference between JWT and session-based authentication?**
> Sessions store state on the server — the user gets a session ID cookie, and the server looks up the session on every request. JWTs store state in the token itself — the server signs a token with user info, the client sends it on every request, and the server just verifies the signature without a database lookup. Sessions are easier to revoke but require a shared store for horizontal scaling. JWTs are stateless and scale easily but cannot be invalidated before expiry.

**Q6: How do you handle JWT revocation?**
> The correct pattern is short-lived access tokens (15 minutes) paired with long-lived refresh tokens. The access token expires quickly, limiting the window if it is stolen. The refresh token is stored in an HttpOnly cookie, is tracked in the database, and can be invalidated server-side on logout. When the access token expires, the client uses the refresh token to get a new one.

**Q7: What is the difference between `no-cache` and `no-store` in Cache-Control?**
> `no-cache` means the browser or CDN may cache the response, but must revalidate it with the server before using it on subsequent requests. `no-store` means never cache at all — the response is always fetched fresh from the server. Use `no-store` for sensitive data like OTPs, bank statements, or personal information.

**Q8: How would you cache a REST API that changes every 60 seconds?**
> Set `Cache-Control: public, s-maxage=60` on the response. CDNs will serve cached responses for up to 60 seconds, absorbing traffic during that window. When the cache expires, the next request reaches the origin server and refreshes the cache. For user-specific data, use `private, max-age=60` so only the browser caches it, not the CDN.

**Q9: Why must every service-to-service HTTP call have a timeout?**
> Without a timeout, a slow downstream service can hold caller threads blocked indefinitely. Under load, this exhausts the thread pool, making the calling service completely unresponsive to all requests — a cascade failure. A timeout limits the blast radius: only requests to the slow service fail, and the caller remains available for other traffic.

**Q10: What is connection pooling and why does it matter?**
> Connection pooling maintains a set of pre-established TCP connections to the database so each request can borrow one instead of creating a new one. Establishing a TCP connection adds round-trip latency and CPU overhead. At high request rates, creating a new connection per request is a significant bottleneck. The pool size must be tuned — too small causes queuing, too large exhausts database connection limits.

**Q11: When would you choose asynchronous service communication over synchronous HTTP?**
> When the operation does not need to complete before responding to the user. For example, after placing an order, I respond to the user immediately and publish an "order.created" event to a message queue. The notification service consumes this event and sends a confirmation email independently. This decouples the services — if the notification service is down, the order still succeeds and the email is sent when the service recovers.

**Q12: What is the REST constraint of statelessness and why does it matter?**
> Statelessness means the server stores no client session state between requests. Every request carries all information needed to process it, including the auth token. This matters for scaling: because any server instance can handle any request, you can add servers behind a load balancer freely without worrying about which server has a user's session. Stateful sessions require a shared session store (Redis) to achieve the same scalability.

---

*Day 2 complete. Day 3 covers: gRPC, message queues (Kafka, RabbitMQ), database networking (connection pooling deep dive), reverse proxies and load balancers, and service discovery.*
