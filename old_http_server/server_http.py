import socket
import json
from urllib.parse import urlparse, parse_qs

HOST = '127.0.0.1'
PORT = 8080

# carrega os dados do arquivo (se existir)
def carregar_dados():
    try:
        with open("dados.json", "r") as f:
            return json.load(f)
    except:
        return []  # se der erro (arquivo não existe), começa vazio

# salva os dados no arquivo
def salvar_dados(dados):
    with open("dados.json", "w") as f:
        json.dump(dados, f, indent=4)

dados = carregar_dados()

# cria o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Servidor HTTP rodando em http://{HOST}:{PORT}")

while True:
    # aceita conexão do navegador
    client, addr = server.accept()

    # recebe a requisição HTTP
    request = client.recv(4096).decode()

    # separa header e body
    parts = request.split("\r\n\r\n")
    header = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    # pega método (GET/POST) e caminho
    method, path, _ = header.split("\n")[0].split()

    # ========================
    # 🔹 GET (buscar)
    # ========================
    if method == "GET":
        parsed = urlparse(path)
        params = parse_qs(parsed.query)

        resultado_html = ""

        # verifica se veio id na URL
        if "id" in params:
            id_busca = params["id"][0]

            encontrado = None

            # percorre lista procurando o id
            for pessoa in dados:
                if pessoa["id"] == id_busca:
                    encontrado = pessoa
                    break

            # se encontrou, mostra os dados
            if encontrado:
                print(f"[GET - {addr}] Busca por id={id_busca} -> encontrado")
                resultado_html = f"""
                <div class="result success">
                    <p><strong>ID:</strong> {encontrado['id']}</p>
                    <p><strong>Nome:</strong> {encontrado['nome']}</p>
                    <p><strong>Idade:</strong> {encontrado['idade']}</p>
                </div>
                """
            else:
                print(f"[GET - {addr}] Busca por id={id_busca} -> nao encontrado")
                resultado_html = "<p> Nao encontrado</p>"
        else:
            resultado_html = "<p>Use ?id=1</p>"

        # página principal
        response_body = f"""
<html>
<head>
    <title>Sistema de Usuarios</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}

        .container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            width: 380px;
            text-align: center;
        }}

        h1 {{
            margin-bottom: 5px;
        }}

        h2 {{
            margin-top: 25px;
            font-size: 18px;
            color: #555;
        }}

        input {{
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border: 1px solid #ccc;
        }}

        button {{
            width: 100%;
            padding: 10px;
            background: #6c63ff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
        }}

        button:hover {{
            background: #574fd6;
        }}

        .result {{
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            text-align: left;
            font-size: 14px;
        }}

        .success {{
            background: #e6f4ea;
            border-left: 5px solid #28a745;
        }}

        .error {{
            background: #fdecea;
            border-left: 5px solid #dc3545;
        }}

        .info {{
            background: #e7f3ff;
            border-left: 5px solid #007bff;
        }}
    </style>
</head>

<body>
    <div class="container">
        <h1> Sistema</h1>
        <p>Buscar usuario por ID</p>

        {resultado_html}

        <!-- formulário GET -->
        <form method="GET">
            <input name="id" placeholder="Digite o ID (ex: 1)">
            <button>Buscar</button>
        </form>

        <h2>Cadastrar novo usuario</h2>

        <!-- formulário POST -->
        <form method="POST">
            <input name="nome" placeholder="Nome">
            <input name="idade" placeholder="Idade">
            <button>Cadastrar</button>
        </form>
    </div>
</body>
</html>
"""

    # ========================
    # 🔹 POST (cadastrar)
    # ========================
    elif method == "POST":
        params = parse_qs(body)

        # pega dados do formulário
        nome = params.get("nome", [""])[0]
        idade = params.get("idade", [""])[0]

        # gera id automático
        novo_id = str(len(dados) + 1)

        novo_usuario = {
            "id": novo_id,
            "nome": nome,
            "idade": idade
        }

        # adiciona na lista
        dados.append(novo_usuario)

        # salva no arquivo
        salvar_dados(dados)

        print(f"[POST - {addr}] Usuario cadastrado -> id={novo_id}, nome={nome}, idade={idade}")

        # resposta após cadastro
        response_body = f"""
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}

        .card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            width: 350px;
        }}

        h1 {{
            color: #333;
        }}

        p {{
            margin: 10px 0;
        }}

        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 15px;
            background: #6c63ff;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }}

        a:hover {{
            background: #574fd6;
        }}
    </style>
</head>

<body>
    <div class="card">
        <h1> Usuario cadastrado</h1>
        <p><strong>Nome:</strong> {nome}</p>
        <p><strong>Idade:</strong> {idade}</p>

        <a href="/">Voltar</a>
    </div>
</body>
</html>
"""

    else:
        print(f"[ERRO] Metodo nao suportado: {method}")
        response_body = "<h1>Método nao suportado</h1>"

    # monta resposta HTTP
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n\r\n"
    response += response_body

    client.sendall(response.encode())
    client.close()