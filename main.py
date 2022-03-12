import socket

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5000
    response = b"""HTTP/1.1 200 OK\n\n<h1>Hello, World</h1>"""

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((HOST, PORT))
    listener.listen(1)
    print(f"The Server Is Listening On https://{HOST}:{PORT}")

    while True:
        client_connection, client_address = listener.accept()
        data = client_connection.recv(1024)
        try:
            print(data.decode('utf-8'))
        except UnicodeDecodeError:
            print("¯\_(ツ)_/¯")

        client_connection.sendall(response)
        client_connection.close()
