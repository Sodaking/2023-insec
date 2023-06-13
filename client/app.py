from local_dns_server import StubResolver
import time
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    client = StubResolver(domain='www.google.com')
    client.start(pki_type="certificates/domain_ecc256", algorithm='sha256')