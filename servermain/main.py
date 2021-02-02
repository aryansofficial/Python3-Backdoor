from server import Server
import threading


server = Server(ip='0.0.0.0', port=5052)
server.connection.bind((server.ip, server.port))
# server.start()

while True:
    server.connection.listen()
    print(f'[LISTENING] Server is listening on {server.ip} {server.port}')
    while True:
        conn, addr = server.connection.accept()
        # server.connList.append((conn, addr))
        server.connList.append(conn)
        server.ipList.append(addr)
        thread = threading.Thread(target=server.handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
