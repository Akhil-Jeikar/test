import socket
import threading
import re
import json

from packages.response import response_handler
from packages.type import type_handler

class Server():
    version='1.0.0.0'

    def __init__(self):
        print("Server Started")
        self.host="127.0.0.1"
        self.port=8080

        self.routes = []
        print("Initial routes",self.routes)
        try:
            self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.s.bind((self.host,self.port))
        except socket.error as e:
            print(f"{e} Failed to Initialise the server")
        else:
            self.s.listen()
            print("Server is lIstening  ")

    def get(self, path):
        def decorator(func):
            param_names = re.findall(r'{(\w+)}', path)
            pattern = re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path)
            compiled_pattern = re.compile(f'^{pattern}$')

            self.routes.append((compiled_pattern, param_names, func, "GET"))
            return func
        return decorator
    
    def post(self, path):
        def decorator(func):
            param_names = re.findall(r'{(\w+)}', path)
            pattern = re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path)
            compiled_pattern = re.compile(f'^{pattern}$')
            self.routes.append((compiled_pattern, param_names, func, "POST"))
            return func
        return decorator

    
    def handle_client(self, client):
        try:
            message = client.recv(4096).decode()
            if not message:
                client.close()
                return
            headers_section, _, body = message.partition('\r\n\r\n')
            request_lines = headers_section.splitlines()
            if not request_lines:
                client.sendall(response_handler(400, "Bad Request", "text/plain").encode())
                return

            method, path, _ = request_lines[0].split(' ')
            response = response_handler(404, "Route not found", "text/plain")
            for pattern, _, func, req_method in self.routes:
                if method != req_method:
                    continue
                match = pattern.match(path)
                if not match:
                    continue
            
                if method == 'GET':
                    params = match.groupdict()
                    response_body = func(**params)

                elif method == 'POST':
                    headers = {}
                    for line in request_lines[1:]:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            headers[key.strip().lower()] = value.strip()
                    url_params = match.groupdict()
                    content_type_header = headers.get("content-type", "")
                    if "application/json" in content_type_header:
                        try:
                            json_body = json.loads(body) if body else {}
                        except json.JSONDecodeError:
                            json_body = {}
                        params = {**url_params, **json_body}
                        response_body = func(**params)
                    elif "text/plain" in content_type_header:
                        response_body = func(body, **url_params)

                    else:
                        response_body = func(**url_params)
                content_type = type_handler(response_body)

                if isinstance(response_body, dict):
                    response_body = json.dumps(response_body)
                print("CLient sent:",response_body)
                response = response_handler(200, response_body, content_type)
            

            client.sendall(response.encode())
        finally:
            client.close()

    def run(self):
        print("Server is running and accepting connections...")
        while True:
            client, add = self.s.accept()
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()





