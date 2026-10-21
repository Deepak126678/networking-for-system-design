"""
DAY 2 — TCP CLIENT
Run tcp_server.py first, then run this.
"""

import socket

HOST = 'localhost'
PORT = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

print(f"[TCP CLIENT] Connecting to {HOST}:{PORT}...")
client.connect((HOST, PORT))  # <-- 3-way handshake happens here!
print(f"[TCP CLIENT] ✅ Connected! (SYN → SYN-ACK → ACK done)")

messages = ["hello", "networking is fun", "tcp guarantees delivery"]

for msg in messages:
    print(f"\n[TCP CLIENT] Sending: '{msg}'")
    client.send(msg.encode())

    response = client.recv(1024)
    print(f"[TCP CLIENT] Got back: '{response.decode()}'")

client.close()
print("\n[TCP CLIENT] Connection closed. (FIN → FIN-ACK → ACK done)")
