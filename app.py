import socket
from routes import handle_request  # função que decide a resposta

HOST = '127.0.0.1'  # localhost 
PORT = 8080         # porta do servidor

if __name__ == '__main__':
    # cria o servidor (TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # conecta o servidor ao endereço e porta
    server.bind((HOST, PORT))
    
    # começa a escutar conexões
    server.listen(1)

    print(f"Servidor HTTP rodando em http://{HOST}:{PORT}")

    while True:
        # espera alguém se conectar
        client, addr = server.accept()
        
        # recebe a requisição (request)
        request = client.recv(8192).decode('utf-8', errors='replace')
        
        # processa a requisição e gera resposta
        response = handle_request(request, addr)
        
        # envia a resposta pro cliente (navegador)
        client.sendall(response.encode('utf-8'))
        
        # fecha a conexão
        client.close()