from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import hashlib


class FileEventHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        post = parse_qs(post_body.decode('utf-8'))
        file_hash = self.generate_file_hash(post['file'][0])

        self.wfile.write(file_hash.encode('utf-8'))
        return

    def generate_file_hash(self, filepath: str):
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()


def run(server_class=HTTPServer, handler_class=FileEventHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
