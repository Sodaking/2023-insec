import socket
import ssl
from OpenSSL import crypto

trusted_root_certificate = "rootCA"

def load_certificate(certificate_file):
    with open(certificate_file + ".crt", "rt") as f:
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    return crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)

def verify_signature(certificate, signature, data):
    try:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
        public_key = cert.get_pubkey()
        pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, public_key)
        return crypto.verify(cert, signature, data, "sha256") == None
    except crypto.Error:
        return False

def verify_certificate_chain(certificate, trusted_cert_pem):
    # Load the certificate
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)

    # Create and configure a X509Store
    store = crypto.X509Store()

    # Add trusted certs to the store
    trusted_cert = crypto.load_certificate(crypto.FILETYPE_PEM, trusted_cert_pem)
    store.add_cert(trusted_cert)

    # Create a X509StoreContext with the cert and the store
    store_ctx = crypto.X509StoreContext(store, cert)

    # Verify the certificate, returns None if successful, raises exception otherwise
    try:
        store_ctx.verify_certificate()
        print("Certificate chain is valid")
        return True
    except Exception as e:
        print(f"Certificate chain Verification failed: {str(e)}")    
        return False

class TCPClient:
    #def __init__(self, host='127.0.0.1', port=8080):
    def __init__(self, host='147.46.242.204', port=9990):
        self.host = host
        self.port = port

    def start(self):
        with socket.create_connection((self.host, self.port)) as sock:
            root_certificate = load_certificate(trusted_root_certificate)
            domain = 'www.naver.com'
            sock.sendall(domain.encode())
            
            data = sock.recv(4096)
            ip, certificate, signature = data.split(b'separator')
            certificate2 = certificate
            is_valid = verify_certificate_chain(certificate, root_certificate)
            if is_valid == False:
                return
    
            is_valid = verify_signature(certificate2, signature, ip)
            if is_valid:
                print('Signature verification OK: ' + ip.decode())
            else:
                print('The server is not legitimate!')

if __name__ == '__main__':
    client = TCPClient()
    client.start()

