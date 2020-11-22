from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

import base64
import hashlib
import os
import requests


class FileEventHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content_length = int(self.headers['Content-Length'])
        post_body = self.rfile.read(content_length)
        post = parse_qs(post_body.decode('utf-8'))
        filename = post['file'][0]
        filename_fragments = filename.split("_")
        source_ip = filename_fragments[0]
        original_filename = "_".join(filename_fragments[1:])
        filepath = post['path'][0] + filename
        file_hash = self.generate_file_hash(filepath=filepath)
        ip_valid = self.validate_ip(source_ip)
        file_valid = self.validate_file_hash(file_hash=file_hash)

        if not file_valid or not ip_valid:
            os.unlink(filepath)
        else:
            os.rename(filepath, post['path'][0] + original_filename)

        return

    @staticmethod
    def generate_file_hash(filepath: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)

        return sha256_hash.hexdigest()

    @staticmethod
    def validate_file_hash(file_hash: str) -> bool:
        credentials = os.getenv("XFE_API_KEY", "") + ":" + os.getenv("XFE_API_PASSWORD", "")
        headers = {
            "Authorization": "Basic " + base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        }
        r = requests.get('https://api.xforce.ibmcloud.com/malware/' + file_hash, headers=headers)
        if r.status_code == 200:
            return False

        return True

    @staticmethod
    def validate_ip(ip: str) -> bool:
        credentials = os.getenv("XFE_API_KEY", "") + ":" + os.getenv("XFE_API_PASSWORD", "")
        headers = {
            "Authorization": "Basic " + base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        }
        r = requests.get('https://api.xforce.ibmcloud.com/ipr/history/' + ip, headers=headers)
        if r.status_code == 200:
            history = r.json()['history']

            for entry in history:
                if entry['score'] > 2:
                    return False

        return True


def run(server_class=HTTPServer, handler_class=FileEventHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


run()
