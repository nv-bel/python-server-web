import socket
from routes import handle_request

HOST = '127.0.0.1'
PORT = 8080

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"Servidor HTTP rodando em http://{HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        request = client.recv(8192).decode('utf-8', errors='replace')
        response = handle_request(request, addr)
        client.sendall(response.encode('utf-8'))
        client.close()
