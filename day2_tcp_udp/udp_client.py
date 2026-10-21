"""
DAY 2 — UDP CLIENT
Fire-and-forget! No connection setup needed.
"""

import socket

HOST = 'localhost'
PORT = 9998

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP

print("[UDP CLIENT] No connection setup — UDP just sends!")
print("[UDP CLIENT] Notice: No SYN, no handshake, just fire datagrams\n")

messages = [
    "packet 1 - may arrive out of order",
    "packet 2 - no delivery guarantee",
    "packet 3 - but very fast!",
]

for msg in messages:
    print(f"[UDP CLIENT] 🚀 Sending: '{msg}'")
    client.sendto(msg.encode(), (HOST, PORT))

    try:
        client.settimeout(2)
        response, _ = client.recvfrom(1024)
        print(f"[UDP CLIENT] Response: '{response.decode()}'")
    except socket.timeout:
        print(f"[UDP CLIENT] ⚠️  No response (timeout) — this is normal for UDP!")

client.close()
print("\n[UDP CLIENT] Done! No FIN handshake needed — just close.")

print("\n--- TCP vs UDP COMPARISON ---")
print("  TCP: SYN → SYN-ACK → ACK → [data] → FIN → FIN-ACK → ACK")
print("  UDP: [data] (that's it!)")
print("  Use TCP for: web, email, file transfer (reliability matters)")
print("  Use UDP for: video calls, gaming, DNS (speed matters)")
