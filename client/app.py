from local_dns_server import StubResolver
import time
import numpy as np

if __name__ == '__main__':
    # test code
    elapsed_time1 = []
    for i in range(1000):
        start_time = time.time()
        client = StubResolver(domain='www.google.com')
        print(client.start(0))
        end_time = time.time()
        elapsed_time1.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time1 = np.array(elapsed_time1)
    mean1 = np.mean(elapsed_time1)
    std1  = np.std(elapsed_time1)
    

    elapsed_time2 = []
    for i in range(1000):
        start_time = time.time()
        client = StubResolver(domain='www.google.com')
        print(client.start(1))
        end_time = time.time()
        elapsed_time2.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time2 = np.array(elapsed_time2)
    mean2 = np.mean(elapsed_time2)
    std2  = np.std(elapsed_time2)
    

    elapsed_time3 = []
    for i in range(1000):
        start_time = time.time()
        client = StubResolver(domain='www.google.com')
        print(client.start(2))
        end_time = time.time()
        elapsed_time3.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time3 = np.array(elapsed_time3)
    mean3 = np.mean(elapsed_time3)
    std3  = np.std(elapsed_time3)
    print(f'domain1. 256 bits - average elapsed_time = {mean1} seconds, std_dev = {std1}')
    print(f'domain2. 2048 bits - average elapsed_time = {mean2} seconds, std_dev = {std2}')
    print(f'domain3. 4096 bits - average elapsed_time = {mean3} seconds, std_dev = {std3}')
