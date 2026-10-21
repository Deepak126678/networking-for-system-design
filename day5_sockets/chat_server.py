"""
DAY 5 — MULTI-CLIENT CHAT SERVER
Each client that connects gets their own thread.
Run this server, then connect multiple clients using chat_client.py
"""

import socket
import threading
from datetime import datetime

HOST = 'localhost'
PORT = 7777

# Track all connected clients: {conn: username}
clients = {}
clients_lock = threading.Lock()

def timestamp():
    return datetime.now().strftime('%H:%M:%S')

def broadcast(message, exclude_conn=None):
    """Send message to all connected clients"""
    with clients_lock:
        dead = []
        for conn in clients:
            if conn != exclude_conn:
                try:
                    conn.send(message.encode())
                except:
                    dead.append(conn)
        for conn in dead:
            del clients[conn]

def handle_client(conn, addr):
    """Handle one connected client in its own thread"""
    try:
        # Get username
        conn.send("Enter your username: ".encode())
        username = conn.recv(1024).decode().strip()

        with clients_lock:
            clients[conn] = username

        print(f"[{timestamp()}] ✅ {username} joined from {addr}")
        broadcast(f"[{timestamp()}] 🟢 {username} joined the chat!\n", exclude_conn=conn)
        conn.send(f"Welcome {username}! You're connected. Type 'quit' to leave.\n".encode())

        # Show who's online
        with clients_lock:
            online = [v for v in clients.values()]
        conn.send(f"Online users: {', '.join(online)}\n\n".encode())

        # Message loop
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()

            if msg.lower() == 'quit':
                break
            elif msg.lower() == 'list':
                with clients_lock:
                    online = [v for v in clients.values()]
                conn.send(f"Online: {', '.join(online)}\n".encode())
            elif msg.lower() == 'ports':
                conn.send(f"Your connection: {addr}\nServer port: {PORT}\n"
                          f"Well-known ports: 80=HTTP, 443=HTTPS, 22=SSH, "
                          f"21=FTP, 25=SMTP, 3306=MySQL, 5432=PostgreSQL\n".encode())
            else:
                broadcast_msg = f"[{timestamp()}] {username}: {msg}\n"
                print(broadcast_msg.strip())
                broadcast(broadcast_msg, exclude_conn=conn)
                conn.send(f"[you → all]: {msg}\n".encode())

    except Exception as e:
        print(f"[{timestamp()}] Error with {addr}: {e}")
    finally:
        with clients_lock:
            username = clients.pop(conn, str(addr))
        conn.close()
        broadcast(f"[{timestamp()}] 🔴 {username} left the chat.\n")
        print(f"[{timestamp()}] {username} disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)

    print(f"{'='*55}")
    print(f"  CHAT SERVER running on {HOST}:{PORT}")
    print(f"{'='*55}")
    print(f"\n  Each client gets its OWN THREAD — that's how servers handle")
    print(f"  multiple connections simultaneously!\n")
    print(f"  Connect with: python chat_client.py")
    print(f"  Or raw: telnet localhost {PORT}\n")
    print(f"  Commands clients can send:")
    print(f"    list  — show online users")
    print(f"    ports — learn about common ports")
    print(f"    quit  — disconnect\n")

    while True:
        conn, addr = server.accept()
        print(f"[{timestamp()}] New connection from {addr} — spawning thread...")
        # Each client runs in its own thread!
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f"[{timestamp()}] Active threads: {threading.active_count() - 1} clients")

if __name__ == '__main__':
    main()
