import os
from urllib.parse import parse_qs, urlparse
from storage import carregar_dados, salvar_dados  # funções que leem/salvam dados

# caminhos das pastas
BASE_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# lê arquivo (html ou css)
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# monta resposta HTTP completa
def build_response(body, status='200 OK', content_type='text/html'):
    headers = [
        f'HTTP/1.1 {status}',  # status da resposta
        f'Content-Type: {content_type}',  # tipo (html, css, etc)
        f'Content-Length: {len(body.encode("utf-8"))}',  # tamanho do conteúdo
        'Connection: close',  # fecha conexão depois
        '',
        ''
    ]
    return '\r\n'.join(headers) + body

# substitui {{ variavel }} no HTML
def render_template(name, context=None):
    html = read_file(os.path.join(TEMPLATE_DIR, name))
    if context is None:
        context = {}
    for key, value in context.items():
        html = html.replace(f'{{{{ {key} }}}}', value)
    return html

# função principal que trata a requisição
def handle_request(request, addr):

    # se não veio nada
    if not request:
        return build_response('<h1>Requisição vazia</h1>', status='400 Bad Request')

    # separa as linhas da requisição
    request_lines = request.split('\r\n')
    request_line = request_lines[0]

    # separa método (GET/POST), caminho e versão HTTP
    parts = request_line.split()
    if len(parts) < 3:
        return build_response('<h1>Requisição inválida</h1>', status='400 Bad Request')

    method, path, _ = parts
    parsed = urlparse(path)  # separa rota e parâmetros

    # ================= GET =================
    if method == 'GET':

        # página principal
        if parsed.path == '/':
            params = parse_qs(parsed.query)  # pega ?id=1
            resultado_html = ''

            # se tem id na URL
            if 'id' in params:
                id_busca = params['id'][0]
                dados = carregar_dados()

                # procura usuário pelo id
                encontrado = next((p for p in dados if p.get('id') == id_busca), None)

                if encontrado:
                    print(f"[GET - {addr}] Busca por id={id_busca} -> encontrado | id={id_busca}, nome={encontrado['nome']}, idade={encontrado['idade']}")
                    
                    # monta HTML com os dados
                    resultado_html = (
                        '<div class="result success">'
                        f'<p><strong>ID:</strong> {encontrado["id"]}</p>'
                        f'<p><strong>Nome:</strong> {encontrado["nome"]}</p>'
                        f'<p><strong>Idade:</strong> {encontrado["idade"]}</p>'
                        '</div>'
                    )
                else:
                    print(f"[GET - {addr}] Busca por id={id_busca} -> não encontrado")
                    resultado_html = '<div class="result error"><p>Usuário não encontrado.</p></div>'
            else:
                resultado_html = '<div class="result info"><p>Use <code>?id=1</code> para buscar.</p></div>'

            # renderiza HTML com resultado
            body = render_template('index.html', {'resultado_html': resultado_html})
            return build_response(body)

        # arquivos estáticos (CSS, etc)
        if parsed.path.startswith('/static/'):
            return serve_static(parsed.path)

        # rota não encontrada
        return build_response('<h1>404 Not Found</h1>', status='404 Not Found')

    # ================= POST =================
    if method == 'POST':

        # pega corpo da requisição (dados do formulário)
        body = request.split('\r\n\r\n', 1)[1] if '\r\n\r\n' in request else ''
        params = parse_qs(body)

        nome = params.get('nome', [''])[0]
        idade = params.get('idade', [''])[0]

        # validação
        if not nome or not idade:
            error_html = '<div class="result error"><p>Nome e idade são obrigatórios.</p></div>'
            body = render_template('index.html', {'resultado_html': error_html})
            return build_response(body)

        # salva novo usuário
        dados = carregar_dados()
        novo_id = str(len(dados) + 1)
        dados.append({'id': novo_id, 'nome': nome, 'idade': idade})
        salvar_dados(dados)

        print(f"[POST - {addr}] Usuario cadastrado -> id={novo_id}, nome={nome}, idade={idade}")

        # página de confirmação
        body = render_template('confirmation.html', {'nome': nome, 'idade': idade})
        return build_response(body)

    # método não suportado
    return build_response('<h1>Método não suportado</h1>', status='405 Method Not Allowed')

# serve arquivos estáticos (CSS)
def serve_static(path):
    filename = path.lstrip('/')
    static_path = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(static_path):
        return build_response('<h1>404 Not Found</h1>', status='404 Not Found')

    content_type = 'text/css' if static_path.endswith('.css') else 'application/octet-stream'
    body = read_file(static_path)
    return build_response(body, content_type=content_type)