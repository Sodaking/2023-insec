import socket
from OpenSSL import crypto
import random

def create_signature(private_key_file, data):
    with open(private_key_file, "rt") as f:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
    return crypto.sign(private_key, data, "sha256")

class TCPServer:
    def __init__(self, host='147.46.242.204', port=9990):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)

            while True:
                newsocket, fromaddr = sock.accept()
                try:
                    data = newsocket.recv(1024)
                    ip = socket.gethostbyname(data).encode()
                    
                    key = random.choice(["domain.key", "bad.key"])
                    print(key)
                    signature = create_signature(key, ip)
                    # print(signature, ip)
                    response = signature + b'separator' + ip
                    newsocket.sendall(response)
                finally:
                    newsocket.close()

if __name__ == '__main__':
    server = TCPServer()
    server.start()