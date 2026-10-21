"""
DAY 6 — LOAD BALANCER
Simulates 3 backend servers + 1 load balancer.
Run this single file — it starts everything automatically!

Architecture:
  Client → Load Balancer (:9000) → Backend 1 (:8001)
                                  → Backend 2 (:8002)
                                  → Backend 3 (:8003)

Test with:
  curl http://localhost:9000
  (run 9 times to see Round Robin distribute to each server 3 times)
"""

import socket
import threading
import itertools
import time
from datetime import datetime

# ── Backend Server ───────────────────────────────────
def start_backend(port, name):
    """A simple backend HTTP server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', port))
    server.listen(10)
    print(f"  [Backend] {name} started on :{port}")

    request_count = 0

    while True:
        try:
            conn, addr = server.accept()
            request_count += 1
            conn.recv(4096)  # read the incoming request

            # Simulate slight processing time differences per server
            time.sleep(0.01)

            body = f"""{{
  "server": "{name}",
  "port": {port},
  "requests_handled": {request_count},
  "timestamp": "{datetime.now().strftime('%H:%M:%S')}",
  "message": "Hello from {name}!"
}}"""
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: application/json\r\n"
                f"Content-Length: {len(body)}\r\n"
                f"X-Served-By: {name}\r\n"
                f"\r\n"
                f"{body}"
            )
            conn.send(response.encode())
            conn.close()
        except Exception as e:
            pass

# ── Load Balancer Strategies ─────────────────────────
class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.round_robin_iter = itertools.cycle(servers)
        self.request_count = 0
        self.server_counts = {s[0]: 0 for s in servers}

    def round_robin(self):
        """Each request goes to the next server in rotation"""
        return next(self.round_robin_iter)

    def get_server(self, strategy="round_robin"):
        if strategy == "round_robin":
            return self.round_robin()

def start_load_balancer(lb_port, backends):
    """The actual load balancer"""
    lb = LoadBalancer(backends)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', lb_port))
    server.listen(50)

    print(f"\n  [LB] Load Balancer started on :{lb_port}")
    print(f"  [LB] Strategy: Round Robin")
    print(f"  [LB] Distributing to: {[b[0] for b in backends]}\n")

    request_num = 0
    while True:
        try:
            client_conn, client_addr = server.accept()
            request_num += 1

            # Pick a backend (Round Robin)
            backend_host, backend_port, backend_name = lb.get_server()
            lb.server_counts[backend_host] += 1

            print(f"  [LB] Request #{request_num} from {client_addr} "
                  f"→ forwarding to {backend_name} (:{backend_port})")

            # Forward to backend
            backend_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            backend_conn.connect((backend_host, backend_port))

            # Forward client request to backend
            request_data = client_conn.recv(4096)
            backend_conn.send(request_data if request_data else b"GET / HTTP/1.0\r\n\r\n")

            # Forward backend response to client
            response = backend_conn.recv(65536)
            client_conn.send(response)

            backend_conn.close()
            client_conn.close()

            # Show distribution stats every 3 requests
            if request_num % 3 == 0:
                total = sum(lb.server_counts.values())
                print(f"\n  [LB] 📊 Distribution after {total} requests:")
                for host, count in lb.server_counts.items():
                    bar = '█' * count
                    print(f"       {host}: {bar} ({count})")
                print()

        except Exception as e:
            pass

# ── Main ─────────────────────────────────────────────
if __name__ == '__main__':
    BACKENDS = [
        ('localhost', 8001, 'Server-1'),
        ('localhost', 8002, 'Server-2'),
        ('localhost', 8003, 'Server-3'),
    ]
    LB_PORT = 9000

    print(f"{'='*55}")
    print(f"  LOAD BALANCER DEMO")
    print(f"{'='*55}")
    print(f"\n  Architecture:")
    print(f"  You → LB(:9000) → Server-1(:8001)")
    print(f"                  → Server-2(:8002)")
    print(f"                  → Server-3(:8003)\n")

    # Start backend servers in background threads
    for host, port, name in BACKENDS:
        t = threading.Thread(target=start_backend, args=(port, name))
        t.daemon = True
        t.start()

    time.sleep(0.5)  # let backends start

    print(f"\n  Test commands (run in another terminal):")
    print(f"  curl http://localhost:{LB_PORT}")
    print(f"  for ($i=1; $i -le 9; $i++) {{ curl http://localhost:{LB_PORT} }}")
    print(f"\n  Watch Round Robin distribute requests evenly!\n")
    print(f"  Discussion questions:")
    print(f"    - What if Server-2 goes down? How to add health checks?")
    print(f"    - When would you use 'Least Connections' instead?")
    print(f"    - What is 'Sticky Session' and why is it needed?\n")

    # Start load balancer (blocks here)
    start_load_balancer(LB_PORT, BACKENDS)
