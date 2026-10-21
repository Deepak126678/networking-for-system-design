"""
DAY 2 — TCP SERVER
Run this first, then run tcp_client.py in another terminal.
Watch the 3-way handshake happen!
"""

import socket

HOST = 'localhost'
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(1)

print(f"[TCP SERVER] Listening on {HOST}:{PORT}")
print("[TCP SERVER] Waiting for client... (3-way handshake will happen on connect)")

conn, addr = server.accept()  # <-- SYN received, SYN-ACK sent, ACK received here
print(f"[TCP SERVER] ✅ Connected by {addr} — 3-way handshake complete!")

while True:
    data = conn.recv(1024)
    if not data:
        print("[TCP SERVER] Client disconnected.")
        break
    message = data.decode()
    print(f"[TCP SERVER] Received: '{message}'")
    response = f"Echo: {message.upper()}"
    conn.send(response.encode())
    print(f"[TCP SERVER] Sent back: '{response}'")

conn.close()
server.close()
print("[TCP SERVER] Server closed.")
