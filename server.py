import socket
from OpenSSL import crypto
import random

pki_list = ["domain", "domain2", "bad"]

def create_signature(private_key_file, data):
    with open(private_key_file + ".key", "rt") as f:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
    return crypto.sign(private_key, data, "sha256")

def load_certificate(certificate_file):
    with open(certificate_file + ".crt", "rt") as f:
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    return crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)

class TCPServer:
    #def __init__(self, host='127.0.0.1', port=8080):
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
                    
                    #signing certificate choose
                    pki_idx = random.choice(range(len(pki_list)))
                    selected_pki = pki_list[pki_idx]
                    print('Signing Certificate: ' + selected_pki)
                    signature = create_signature(selected_pki, ip)

                    #response certificate choose
                    pki_idx = random.choice(range(len(pki_list)))
                    selected_pki = pki_list[pki_idx]
                    certificate = load_certificate(selected_pki)
                    print('Delivered Certificate: ' + selected_pki)

                    response = ip + b'separator' + certificate + b'separator' + signature
                    newsocket.sendall(response)
                finally:
                    newsocket.close()

if __name__ == '__main__':
    server = TCPServer()
    server.start()