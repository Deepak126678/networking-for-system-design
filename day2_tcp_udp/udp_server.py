"""
DAY 2 — UDP SERVER
No handshake! Just fire and receive.
Run this first, then run udp_client.py
"""

import socket

HOST = 'localhost'
PORT = 9998

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
server.bind((HOST, PORT))

print(f"[UDP SERVER] Listening on {HOST}:{PORT}")
print("[UDP SERVER] No handshake needed — UDP is connectionless!")
print("[UDP SERVER] Waiting for datagrams...\n")

while True:
    data, addr = server.recvfrom(1024)  # no connection, just receive datagram
    message = data.decode()
    print(f"[UDP SERVER] 📦 Datagram from {addr}: '{message}'")
    # UDP: we CAN reply but there's no guarantee client receives it
    server.sendto(f"Got it: {message}".encode(), addr)
