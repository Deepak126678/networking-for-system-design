"""
DAY 5 — CHAT CLIENT
Connect to the chat server. Open multiple terminals and run this
to simulate multiple users chatting!
"""

import socket
import threading
import sys

HOST = 'localhost'
PORT = 7777

def receive_messages(sock):
    """Continuously receive and print messages from server"""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[Disconnected from server]")
                break
            print(data.decode(), end='', flush=True)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"❌ Could not connect to {HOST}:{PORT}")
        print("   Make sure chat_server.py is running first!")
        sys.exit(1)

    print(f"✅ Connected to chat server at {HOST}:{PORT}")
    print(f"   Your socket: {client.getsockname()} → {client.getpeername()}")
    print(f"   (socket = IP + Port, this is YOUR unique connection)\n")

    # Background thread to receive messages
    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    # Send messages
    while True:
        try:
            msg = input()
            client.send(msg.encode())
            if msg.lower() == 'quit':
                break
        except (KeyboardInterrupt, EOFError):
            client.send(b'quit')
            break

    client.close()

if __name__ == '__main__':
    main()
