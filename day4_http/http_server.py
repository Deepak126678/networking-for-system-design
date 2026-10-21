"""
DAY 4 — HTTP SERVER
A mini HTTP server that handles GET, POST, PUT, DELETE requests.
Run this, then open browser at http://localhost:8080
Or use: curl http://localhost:8080
        curl -X POST http://localhost:8080/users -d '{"name":"deepak"}'
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

# In-memory "database"
users_db = [
    {"id": 1, "name": "Deepak", "role": "developer"},
    {"id": 2, "name": "Friend", "role": "developer"},
]

class NetworkingHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {self.command} {self.path} → {args[1]}")

    def send_json(self, status_code, data):
        """Helper to send JSON response"""
        body = json.dumps(data, indent=2).encode()
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.send_header('X-Server', 'NetworkingWeek/1.0')  # custom header!
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        """Read request body"""
        length = int(self.headers.get('Content-Length', 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    # ── GET ──────────────────────────────────────────
    def do_GET(self):
        if self.path == '/':
            self.send_json(200, {
                "message": "Welcome to Networking Week API!",
                "endpoints": {
                    "GET /users":       "List all users",
                    "GET /users/1":     "Get user by ID",
                    "POST /users":      "Create a user",
                    "PUT /users/1":     "Update a user",
                    "DELETE /users/1":  "Delete a user",
                    "GET /status":      "Server status",
                },
                "http_methods": {
                    "GET":    "Read data (safe, idempotent)",
                    "POST":   "Create new resource (not idempotent)",
                    "PUT":    "Update/replace resource (idempotent)",
                    "DELETE": "Remove resource (idempotent)",
                    "PATCH":  "Partial update (not always idempotent)",
                }
            })

        elif self.path == '/users':
            self.send_json(200, {"users": users_db, "count": len(users_db)})

        elif self.path.startswith('/users/'):
            try:
                user_id = int(self.path.split('/')[-1])
                user = next((u for u in users_db if u['id'] == user_id), None)
                if user:
                    self.send_json(200, user)
                else:
                    self.send_json(404, {"error": "User not found", "status": 404,
                                         "tip": "404 = Not Found"})
            except:
                self.send_json(400, {"error": "Invalid ID", "status": 400,
                                      "tip": "400 = Bad Request (your fault!)"})

        elif self.path == '/status':
            self.send_json(200, {
                "status": "running",
                "users_count": len(users_db),
                "status_codes": {
                    "2xx": "Success",
                    "3xx": "Redirection",
                    "4xx": "Client Error (YOUR fault)",
                    "5xx": "Server Error (SERVER's fault)",
                    "200": "OK", "201": "Created", "204": "No Content",
                    "301": "Moved Permanently", "302": "Found (temp redirect)",
                    "400": "Bad Request", "401": "Unauthorized (not logged in)",
                    "403": "Forbidden (logged in but no permission)",
                    "404": "Not Found", "429": "Too Many Requests",
                    "500": "Internal Server Error", "502": "Bad Gateway",
                    "503": "Service Unavailable",
                }
            })
        else:
            self.send_json(404, {"error": f"Route '{self.path}' not found"})

    # ── POST ─────────────────────────────────────────
    def do_POST(self):
        if self.path == '/users':
            body = self.read_body()
            if 'name' not in body:
                self.send_json(400, {"error": "name field is required"})
                return
            new_user = {
                "id": len(users_db) + 1,
                "name": body['name'],
                "role": body.get('role', 'user')
            }
            users_db.append(new_user)
            self.send_json(201, {"message": "User created!", "user": new_user,
                                  "tip": "201 = Created (not 200!)"})
        else:
            self.send_json(404, {"error": "Route not found"})

    # ── PUT ──────────────────────────────────────────
    def do_PUT(self):
        if self.path.startswith('/users/'):
            user_id = int(self.path.split('/')[-1])
            body = self.read_body()
            user = next((u for u in users_db if u['id'] == user_id), None)
            if user:
                user.update(body)
                self.send_json(200, {"message": "User updated!", "user": user})
            else:
                self.send_json(404, {"error": "User not found"})

    # ── DELETE ───────────────────────────────────────
    def do_DELETE(self):
        if self.path.startswith('/users/'):
            user_id = int(self.path.split('/')[-1])
            global users_db
            original_len = len(users_db)
            users_db = [u for u in users_db if u['id'] != user_id]
            if len(users_db) < original_len:
                self.send_json(200, {"message": f"User {user_id} deleted",
                                      "tip": "Some APIs return 204 No Content"})
            else:
                self.send_json(404, {"error": "User not found"})


if __name__ == '__main__':
    PORT = 8080
    server = HTTPServer(('localhost', PORT), NetworkingHandler)
    print(f"{'='*55}")
    print(f"  HTTP SERVER RUNNING on http://localhost:{PORT}")
    print(f"{'='*55}")
    print("\n  Try these commands in another terminal:")
    print(f"  curl http://localhost:{PORT}/")
    print(f"  curl http://localhost:{PORT}/users")
    print(f"  curl http://localhost:{PORT}/users/1")
    print(f"  curl http://localhost:{PORT}/status")
    print(f'  curl -X POST http://localhost:{PORT}/users -H "Content-Type: application/json" -d \'{{"name":"Alice"}}\'')
    print(f"  curl -X DELETE http://localhost:{PORT}/users/1")
    print(f"\n  Press Ctrl+C to stop\n")
    server.serve_forever()
