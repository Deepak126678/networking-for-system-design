# Project Synopsis & Architecture Specification

## Project Title
**Production-Grade Distributed Microservices Infrastructure: High-Performance Nginx L7 Reverse Proxy, Load Balancer & Redis Cache**

**Document Version:** 2.0.0  
**Target Roles:** Software Development Engineer (SDE / SDE-2) / Backend Engineer  
**Architecture Focus:** Production Networking & Microservices System Design  

---

## 1. Executive Summary

In high-scale enterprise architectures (such as Swiggy, Zomato, Netflix, and Amazon), client requests never hit backend application runtimes directly. Instead, battle-tested edge proxies like **Nginx** intercept, secure, cache, and distribute traffic across a fleet of microservices.

This project delivers hands-on industry exposure by architecting, deploying, and benchmarking a complete production networking layer:
- **Nginx** as a Layer 7 Reverse Proxy and Load Balancer managing traffic distribution.
- **Multiple Backend Microservices** handling business operations (Catalog & Order services).
- **Redis** as a high-speed distributed cache and rate limiter.
- **Docker & Docker Compose** orchestrating the isolated multi-container network.

---

## 2. System Resource Allocation & Hardware Footprint

The architecture is designed to run efficiently with lightweight memory utilization and low system overhead:

| Component | Memory Allocation (RAM) | Architectural Characteristics |
|---|---|---|
| **Nginx** | **~10 MB RAM** | C-based asynchronous event-driven I/O model (`epoll`) with minimal overhead. |
| **Redis** | **~15 MB RAM** | High-throughput in-memory data store for caching and distributed rate-limiting counters. |
| **Backend Services** | **~50–100 MB RAM** | Stateless, lightweight microservice runtimes with bounded resource limits. |
| **Docker Engine** | Standard Container Overhead | Containerized network virtualization over isolated bridge subnets. |

**Total Runtime Footprint:** **< 200 MB RAM** across the entire multi-service mesh.

---

## 3. Real-World Architectural Blueprint

```mermaid
flowchart TD
    Client["Client (Browser / Postman / cURL)"] -->|"HTTP/HTTPS on Port 80 / 443"| Nginx["1. Nginx L7 Reverse Proxy & Load Balancer\n- TLS Termination & SSL Offloading\n- Rate Limiting (limit_req zone)\n- Path-Based Routing\n- Upstream Round-Robin Balancing\n- In-Memory Response Caching"]

    subgraph Internal_Private_Network ["Docker Internal Network (Private Subnet 172.20.0.0/16)"]
        Nginx -->|"Path: /api/v1/catalog"| CatalogCluster["Catalog Service Cluster\n- Node A (:5001)\n- Node B (:5002)\n(Load Balanced via Round-Robin)"]
        
        Nginx -->|"Path: /api/v1/orders"| OrderService["Order Service (:6001)"]
        
        CatalogCluster <-->|"Query & Cache Results (Sub-millisecond)"| Redis[("Redis Distributed Cache (:6379)\n- Query Result Caching\n- Distributed Rate Limit Counters")]
        OrderService <-->|"Idempotency & Session Lock"| Redis
    end
```

---

## 4. Core Features & Architecture Specifications

### 1. Nginx Layer 7 Load Balancing & Reverse Proxy
- **Upstream Pool Configuration:** Distribute traffic evenly across multiple instances of backend services using **Round Robin** and **Least Connections**.
- **Active & Passive Health Checks:** Automatically remove dead or crashing backend instances so users never experience 502/504 Bad Gateway errors.
- **Path-Based Routing:** Route traffic based on URL prefixes:
  - `/api/v1/catalog` $\to$ Catalog Service Cluster
  - `/api/v1/orders` $\to$ Order Service Cluster
  - `/static/` $\to$ Direct Nginx kernel-level file serving (`sendfile`)

### 2. Edge Security & Traffic Regulation
- **Rate Limiting:** Protect backends against traffic surges and denial-of-service attempts using Nginx's leaky bucket rate-limiting zones (`limit_req_zone`).
- **Header Injection & Observability:**
  - Inject `X-Request-Id` for distributed end-to-end tracing.
  - Forward real client IP addresses using `X-Forwarded-For` and `X-Real-IP`.

### 3. High-Speed Distributed Caching (Redis)
- Implement cache-aside architecture: Backend checks Redis before querying the database.
- Cache popular catalog queries with a strict TTL (Time to Live) to shield downstream resources.

### 4. Containerized Multi-Service Orchestration (Docker Compose)
- Define the entire networking environment in a single `docker-compose.yml`.
- Set up private network bridging so backend containers are inaccessible from the open internet, leaving Nginx as the single secure entry point.

---

## 5. Practical Engineering Outcomes

1. **Event-Driven Concurrency:** Understanding why Nginx uses an asynchronous event loop (`epoll`) instead of thread-per-connection architectures.
2. **Dynamic Failover:** Configuring upstream blocks in `nginx.conf` and handling node failovers without downtime.
3. **Distributed Caching Strategies:** Integrating Redis to cut database read latency and mitigate cache stampedes.
4. **Container Network Isolation:** Managing Docker bridge networks, container DNS discovery, and port mappings.

---

## 6. Verification & Benchmarking

- **Functional Testing:** Verify load balancing by observing consecutive requests alternating across backend nodes.
- **Failover Simulation:** Stop one backend container (`docker stop catalog-node-2`) and verify that Nginx seamlessly diverts 100% of traffic to healthy nodes without user-facing errors.
- **Load Benchmark:** Use Apache Bench (`ab`) to simulate 10,000 requests across 100 concurrent connections:
  ```powershell
  ab -n 10000 -c 100 http://localhost/api/v1/catalog
  ```

---

## 7. Resume & Professional Summary

> **Production Distributed System Infrastructure (Nginx, Redis, Docker)**  
> *Architected and deployed a multi-service backend infrastructure utilizing Nginx as a Layer 7 reverse proxy and load balancer with path-based routing, rate limiting, and upstream health monitoring. Integrated Redis for distributed caching and session state management. Orchestrated isolated multi-container networking via Docker Compose. Benchmarked traffic routing under high concurrency achieving sub-5ms proxy overhead.*
