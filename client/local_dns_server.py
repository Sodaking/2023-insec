import socket
import ssl
from OpenSSL import crypto
import dns.resolver
import base64

trusted_root_certificate = "certificates/rootCA"

def load_certificate(certificate_file):
    with open(certificate_file + ".crt", "rt") as f:
        certificate = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())
    return crypto.dump_certificate(crypto.FILETYPE_PEM, certificate)

def verify_signature(certificate, signature, data):
    try:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, certificate)
        public_key = cert.get_pubkey()
        pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, public_key)
        crypto.verify(cert, signature, data.encode(), "sha256")
        return True
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
        # print("Certificate chain is valid")
        return True
    except Exception as e:
        # print(f"Certificate chain Verification failed: {str(e)}")    
        return False

def resolve_domain(domain):
    resolver = dns.resolver.Resolver()
    answer = resolver.resolve(domain, 'A')  # query for A records
    for rec in answer:
        print(rec)
    return [record.to_text() for record in answer]

class StubResolver:
    def __init__(self, domain='www.naver.com', host='127.0.0.1', port=8080):
    #def __init__(self, domain='www.naver.com', host='147.46.242.204', port=9990):
        self.host = host
        self.port = port
        self.domain = domain

    def start(self, index):
        with socket.create_connection((self.host, self.port)) as sock:
            root_certificate = load_certificate(trusted_root_certificate)
            message = f"{self.domain}:{index}"
            sock.sendall(self.domain.encode())
            data = sock.recv(4096).decode()

            Name, Ttl, Class, Type, Data, Signature_base64, Certificate_base64 = data.split(':')
            ip, signature, certificate = Data, base64.b64decode(Signature_base64), base64.b64decode(Certificate_base64)

            if Name != self.domain:
                return 'Domain name does not match!'
            # print('Domain name verification OK')

            if Type != 'A':
                return 'Type does not match!'
            # print('Type verification OK')

            if Class != 'IN':
                return 'Class does not match!'
            # print('Class verification OK')

            if verify_signature(certificate, signature, ip) == False:
                return 'Signature verification failed!'
            # print('Signature verification OK')
            
            if verify_certificate_chain(certificate, root_certificate) == False:
                return 'Certificate chain is not valid!'
            # print('Certificate chain verification OK')
            
            return 'IP address: ' + ip

if __name__ == '__main__':
    client = StubResolver(domain='www.naver.com')
    client.start()

