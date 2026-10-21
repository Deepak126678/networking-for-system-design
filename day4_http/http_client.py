"""
DAY 4 — HTTP CLIENT
Tests all endpoints of the HTTP server.
Run http_server.py first, then run this.
"""

import urllib.request
import urllib.error
import json

BASE = "http://localhost:8080"

def print_section(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")

def make_request(method, path, body=None):
    url = BASE + path
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    if body:
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as res:
            status = res.status
            response_body = json.loads(res.read())
            return status, response_body
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

# ── GET / ────────────────────────────────────────────
print_section("GET / — Welcome & API Info")
status, body = make_request("GET", "/")
print(f"  Status: {status}")
print(f"  Endpoints available: {list(body['endpoints'].keys())}")

# ── GET /users ───────────────────────────────────────
print_section("GET /users — List All Users")
status, body = make_request("GET", "/users")
print(f"  Status: {status}")
print(f"  Users: {body['users']}")
print(f"  Count: {body['count']}")

# ── GET /users/1 ─────────────────────────────────────
print_section("GET /users/1 — Get Single User")
status, body = make_request("GET", "/users/1")
print(f"  Status: {status}")
print(f"  User: {body}")

# ── GET /users/999 (404 test) ────────────────────────
print_section("GET /users/999 — 404 Not Found Test")
status, body = make_request("GET", "/users/999")
print(f"  Status: {status} ← This is a 404!")
print(f"  Error: {body['error']}")
print(f"  Tip: {body['tip']}")

# ── POST /users ──────────────────────────────────────
print_section("POST /users — Create New User (201 Created)")
status, body = make_request("POST", "/users", {"name": "Alice", "role": "designer"})
print(f"  Status: {status} ← 201, not 200!")
print(f"  Created: {body['user']}")

# ── GET /users after POST ────────────────────────────
print_section("GET /users — Verify Alice Was Added")
status, body = make_request("GET", "/users")
print(f"  Status: {status}")
print(f"  All users now: {[u['name'] for u in body['users']]}")

# ── PUT /users/1 ─────────────────────────────────────
print_section("PUT /users/1 — Update User (Idempotent)")
status, body = make_request("PUT", "/users/1", {"name": "Deepak Kumar", "role": "senior developer"})
print(f"  Status: {status}")
print(f"  Updated: {body['user']}")

# ── DELETE /users/2 ──────────────────────────────────
print_section("DELETE /users/2 — Remove a User")
status, body = make_request("DELETE", "/users/2")
print(f"  Status: {status}")
print(f"  Message: {body['message']}")

# ── GET /status — Status Codes Reference ─────────────
print_section("GET /status — HTTP Status Codes Reference")
status, body = make_request("GET", "/status")
print(f"  Status: {status}")
print("\n  HTTP Status Code Groups:")
for code, meaning in body['status_codes'].items():
    if len(code) == 3:
        print(f"    {code} → {meaning}")

print("\nDay 4 complete! You just built and tested a REST API from scratch!\n")
