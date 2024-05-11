from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Endpoint "/hello" : Exécute la fonction hello()
        if self.path == "/hello":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = self.hello()
            self.wfile.write(response.encode())

        # Endpoint "/goodbye" : Exécute la fonction goodbye()
        elif self.path == "/goodbye":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = self.goodbye()
            self.wfile.write(response.encode())

        # Endpoint par défaut : Renvoie une page d'accueil
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response = self.home()
            self.wfile.write(response.encode())

    def hello(self):
        return "<html><body><h1>Hello, World!</h1></body></html>"

    def goodbye(self):
        return "<html><body><h1>Goodbye, World!</h1></body></html>"

    def home(self):
        return "<html><body><h1>Welcome to the Home Page</h1></body></html>"

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
