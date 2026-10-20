from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json

APP_VERSION = os.getenv("APP_VERSION", "v1")

class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = {
                "status": "healthy",
                "version": APP_VERSION
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(body).encode())
        elif self.path == "/":
            body = f"Week 9 CI/CD Demo - {APP_VERSION}\n"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(body.encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), AppHandler)
    print(f"Application running on port 8000, version {APP_VERSION}")
    server.serve_forever()
