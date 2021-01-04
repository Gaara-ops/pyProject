import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('127.0.0.1', 8801))
serversocket.listen(5)

print('starting accept..')
while True:
    print('start one accept...')
    conn, c_addr = serversocket.accept()
    print(conn, c_addr)

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print('client data:', data)

            conn.send(data.upper())
        except ConnectionResetError:
            break
    conn.close()

serversocket.close()
