from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, status: int, body: str, content_type="application/json"):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(encoded)

    # GET
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path == "/ping":
            body = json.dumps({"status": "ok", "params": params})
            self._send_response(200, body)

        elif parsed.path == "/echo":
            name = params.get("name", ["World"])[0]
            body = json.dumps({"message": f"Hello, {name}!"})
            self._send_response(200, body)

        else:
            self._send_response(404, json.dumps({"error": "Not Found"}))

    # POST
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_body)
        except json.JSONDecodeError:
            self._send_response(400, json.dumps({"error": "Invalid JSON"}))
            return

        if self.path == "/echo":
            body = json.dumps({"received": payload})
            self._send_response(200, body)

        elif self.path == "/sum":
            nums = payload.get("numbers", [])
            body = json.dumps({"result": sum(nums)})
            self._send_response(200, body)

        else:
            self._send_response(404, json.dumps({"error": "Not Found"}))

    # Silencia logs no terminal (opcional)
    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), RequestHandler)
    print("Servidor rodando em http://localhost:8080")
    server.serve_forever()
