import socket

host = '192.168.0.24'
port = 8000

connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connexion.bind((host, port))
connexion.listen(1)
while True:
    conn, address = connexion.accept()
    with conn:
        print(f"Connected by {address}")
        buff = conn.recv(1024)
        if not buff:
            break
        message = buff.decode('utf-8')
        conn.sendall(f"{message}".encode('utf-8'))