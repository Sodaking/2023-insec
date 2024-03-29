import socket
from OpenSSL import crypto
import random
import base64

pki_list =pki_list = ["certificates/domain_ecc256", "certificates/domain", "certificates/domain_4096", "certificates/bad"]

def create_signature(private_key_file, data, algorithm):
    with open(private_key_file + ".key", "rt") as f:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
    return crypto.sign(private_key, data, algorithm)

def load_certificate(certificate_file):
    with open(certificate_file + ".crt", "rt") as f:
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    return crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)

class TCPServer:
    #def __init__(self, host='127.0.0.1', port=8080):
    def __init__(self, host='147.46.242.204', port=9991):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)

            while True:
                newsocket, fromaddr = sock.accept()
                try:
                    data = newsocket.recv(1024).decode()
                    domain, algorithm, pki_type = data.split(':')
                    

                    ip = socket.gethostbyname(domain)

                    if pki_type == 'none':
                        response = f"{domain}:3600:IN:A:{ip}".encode()
                        newsocket.sendall(response)
                    else:
                    
                        #signing certificate choose
                        if pki_type == 'random':
                            pki_idx = random.choice(range(len(pki_list)))
                            selected_pki = pki_list[pki_idx]
                        else:
                            selected_pki = pki_type
                        # print('Signing Certificate: ' + selected_pki)
                        signature = create_signature(selected_pki, ip.encode(), algorithm)
                        signature_base64 = base64.b64encode(signature).decode()

                        #response certificate choose
                        if pki_type == 'random':
                            pki_idx = random.choice(range(len(pki_list)))
                            selected_pki = pki_list[pki_idx]
                        else:
                            selected_pki = pki_type
                        # print('Delivered Certificate: ' + selected_pki)
                        certificate = load_certificate(selected_pki)
                        certificate_base64 = base64.b64encode(certificate).decode()

                        response = f"{domain}:3600:IN:A:{ip}:{signature_base64}:{certificate_base64}".encode()
                        newsocket.sendall(response)
                    
                finally:
                    newsocket.close()

if __name__ == '__main__':
    server = TCPServer()
    server.start()