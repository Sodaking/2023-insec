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




# import socket
# import ssl

# class TCPServer:
#     def __init__(self, host='127.0.0.1', port=9999):
#         self.host = host
#         self.port = port

#     def start(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#             sock.bind((self.host, self.port))
#             sock.listen(5)
#             sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#             # SSL context 설정
#             context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#             context.load_cert_chain(certfile="domain.crt", keyfile="domain.key")
#             context.verify_mode = ssl.CERT_NONE

#             while True:
#                 newsocket, fromaddr = sock.accept()
#                 try:
#                     connstream = context.wrap_socket(newsocket, server_side=True)
#                     print('Connected by', fromaddr)
#                     while True:
#                         data = connstream.recv(1024)
#                         print(data)
#                         if not data: break
#                         print(socket.gethostbyname(data.decode()))
#                         connstream.sendall(socket.gethostbyname(data.decode()).encode())
#                 except ssl.SSLError as e:
#                     print(f"SSL error occurred: {e}")
#                     connstream.shutdown(socket.SHUT_RDWR)
#                     connstream.close()
#                 except Exception as e:
#                     print("Unexpected error:", e)
#                 finally:
#                     connstream.shutdown(socket.SHUT_RDWR)
#                     connstream.close()

# if __name__ == '__main__':
#     server = TCPServer()
#     server.start()




# import socket
# import ssl

# class TCPServer:
#     def __init__(self, host='127.0.0.1', port=9999):
#         self.host = host
#         self.port = port

#     def start(self):
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
#             sock.bind((self.host, self.port))
#             sock.listen(5)
#             sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#             # SSL context 설정
#             context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#             context.load_cert_chain(certfile="domain.crt", keyfile="domain.key")

#             while True:
#                 newsocket, fromaddr = sock.accept()
#                 connstream = context.wrap_socket(newsocket, server_side=True)
#                 try:
#                     print('Connected by', fromaddr)
#                     while True:
#                         data = connstream.recv(1024)
#                         print(data)
#                         if not data: break
#                         print(socket.gethostbyname(data))
#                         connstream.sendall(socket.gethostbyname(data).encode())
#                 finally:
#                     connstream.shutdown(socket.SHUT_RDWR)
#                     connstream.close()

# if __name__ == '__main__':
#     server = TCPServer()
#     server.start()
