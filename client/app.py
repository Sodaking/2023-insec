from local_dns_server import StubResolver


if __name__ == '__main__':
    client = StubResolver(domain='www.google.com')
    print(client.start())

