import socket
import ssl
from OpenSSL import crypto

def verify_signature(public_key_file, signature, data):
    with open(public_key_file, "rt") as f:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
        public_key = cert.get_pubkey()
        pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, public_key)
    try:
        return crypto.verify(cert, signature, data, "sha256") == None
    except crypto.Error:
        return False

    
class TCPClient:
    def __init__(self, host='147.46.242.204', port=9990):
        self.host = host
        self.port = port

    def start(self):
        with socket.create_connection((self.host, self.port)) as sock:
            domain = 'www.naver.com'
            sock.sendall(domain.encode())
            
            data = sock.recv(1024)
            signature, ip = data.split(b'separator')
            # print(signature, ip)


            is_valid = verify_signature("domain.crt", signature, ip)
            if is_valid:
                print(ip.decode())
            else:
                print('The server is not legitimate!')

if __name__ == '__main__':
    client = TCPClient()
    client.start()

