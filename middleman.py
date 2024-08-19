import os
import base64
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

gdps = "https://platinum.141412.xyz/"
name = "PlatinumGDPS"
PORT = 3000


def xor_cipher(string, key):
    return ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(string))


def encode_gjp(passwd):
    encoded = xor_cipher(passwd, '37526')
    encoded_base64 = base64.b64encode(encoded.encode()).decode()
    modified_base64 = encoded_base64.replace('+', '-').replace('/', '_')
    return modified_base64


def get_gjp():
    gjp = os.getenv("gjp", None)
    if not gjp:
        password = os.getenv("password", None)
        if password:
            gjp = encode_gjp(password)
            with open("./.env", "a") as f:
                f.write(f"\ngjp={gjp}")
        else:
            gjp = "null"
            print(f"You need to (refresh) login in order to use {name} 1.9!\nLogin: Gear Icon => Account\nRefresh: Gear "
                  f"Icon => Account => More => Refresh Login")
    return gjp


debug = os.getenv("debug", "false").lower() == "true"


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            path = urlparse(self.path).path
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()
            post_body = parse_qs(post_data)

            if debug:
                print(f"{path}\n\n{post_body}")

            if 'accountID' in post_body:
                post_body['gjp'] = [get_gjp()]

            response = requests.post(f"{gdps}/{path}", data=post_body, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })

            if debug:
                print(response.text)

            check = response.text

            if path.endswith("loginGJAccount.php") and not check.startswith("-"):
                local_gjp = encode_gjp(post_body.get('password', [''])[0])
                with open("./.env", "a") as file:
                    file.write(f"\ngjp={local_gjp}")
                print(f"Logged in as {post_body.get('userName', [''])[0]}!")

            self.send_response(response.status_code)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.text.encode())

        except Exception as error:
            print('Error:', error)
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Internal Server Error')


def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=PORT):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"QuoicouGJP is running on port {port}!")
    httpd.serve_forever()
