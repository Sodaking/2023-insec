from local_dns_server import StubResolver
import time
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    client = StubResolver(domain='www.google.com')
    # print(client.start(pki_type='random'))
    num = 200
    time_ = []
    for i in range(num):

        start_time = time.time()
        client.start(pki_type='none')
        end_time = time.time()
        time_.append(end_time - start_time)
    mean = np.mean(time_)
    std  = np.std(time_)
    se = std / np.sqrt(num)


    print(f'plain text - average elapsed_time = {mean} seconds, std_dev = {std}')


    
    elapsed_time1 = []
    for i in range(num):
        start_time = time.time()
        client.start(pki_type="certificates/domain_ecc256")
        end_time = time.time()
        elapsed_time1.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time1 = np.array(elapsed_time1)
    mean1 = np.mean(elapsed_time1)
    std1  = np.std(elapsed_time1)
    se1 = std1 / np.sqrt(num)
    

    elapsed_time2 = []
    for i in range(num):
        start_time = time.time()
        client.start(pki_type="certificates/domain")
        end_time = time.time()
        elapsed_time2.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time2 = np.array(elapsed_time2)
    mean2 = np.mean(elapsed_time2)
    std2  = np.std(elapsed_time2)
    se2 = std2 / np.sqrt(num)
    

    elapsed_time3 = []
    for i in range(num):
        start_time = time.time()
        client.start(pki_type="certificates/domain_4096")
        end_time = time.time()
        elapsed_time3.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time3 = np.array(elapsed_time3)
    mean3 = np.mean(elapsed_time3)
    std3  = np.std(elapsed_time3)
    se3 = std3 / np.sqrt(num)

    print(f'domain1. 256 bits - average elapsed_time = {mean1} seconds, std_dev = {std1}')
    print(f'domain2. 2048 bits - average elapsed_time = {mean2} seconds, std_dev = {std2}')
    print(f'domain3. 4096 bits - average elapsed_time = {mean3} seconds, std_dev = {std3}')

    #draw jitter scatter plot with elapsed_time


    jitter = 0.05

    # Scatter plots
    plt.scatter([1] * num + np.random.normal(0, jitter, num), elapsed_time1, s=10, color='red', label='256 bits')
    plt.scatter([2] * num + np.random.normal(0, jitter, num), elapsed_time2, s=10, color='blue', label='2048 bits')
    plt.scatter([3] * num + np.random.normal(0, jitter, num), elapsed_time3, s=10, color='green', label='4096 bits')

    # Labels and legend
    plt.xlabel('index')
    plt.ylabel('elapsed_time')
    plt.legend()

    plt.savefig('certificate_bits.png')
    plt.clf()

      # Scatter plots
    plt.scatter([0] * num + np.random.normal(0, jitter, num), time_, s=10, color='black', label='plain text')
    plt.scatter([1] * num + np.random.normal(0, jitter, num), elapsed_time1, s=10, color='red', label='256 bits')
    plt.scatter([2] * num + np.random.normal(0, jitter, num), elapsed_time2, s=10, color='blue', label='2048 bits')
    plt.scatter([3] * num + np.random.normal(0, jitter, num), elapsed_time3, s=10, color='green', label='4096 bits')

    # Labels and legend
    plt.xlabel('index')
    plt.ylabel('elapsed_time')
    plt.legend()

    plt.savefig('certificate_bits_with_plain.png')
    plt.clf()






    pki_type="certificates/domain_ecc256"

    elapsed_time1 = []
    for i in range(num):
        start_time = time.time()
        client.start(algorithm="sha1", pki_type=pki_type)
        end_time = time.time()
        elapsed_time1.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time1 = np.array(elapsed_time1)
    mean1 = np.mean(elapsed_time1)
    std1  = np.std(elapsed_time1)
    se1 = std1 / np.sqrt(num)
    

    elapsed_time2 = []
    for i in range(num):
        start_time = time.time()
        client.start(algorithm="sha256", pki_type=pki_type)
        end_time = time.time()
        elapsed_time2.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time2 = np.array(elapsed_time2)
    mean2 = np.mean(elapsed_time2)
    std2  = np.std(elapsed_time2)
    se2 = std2 / np.sqrt(num)
    

    elapsed_time3 = []
    for i in range(num):
        start_time = time.time()
        client.start(algorithm="sha512", pki_type=pki_type)
        end_time = time.time()
        elapsed_time3.append(end_time - start_time)
        #print(1)
    #elapsed_time의 분산과 평균 구하기
    elapsed_time3 = np.array(elapsed_time3)
    mean3 = np.mean(elapsed_time3)
    std3  = np.std(elapsed_time3)
    se3 = std3 / np.sqrt(num)

    print(f'sha1 160 bits - average elapsed_time = {mean1} seconds, std_dev = {std1}')
    print(f'sha256 256 bits - average elapsed_time = {mean2} seconds, std_dev = {std2}')
    print(f'sha512 512 bits - average elapsed_time = {mean3} seconds, std_dev = {std3}')

    #draw jitter scatter plot with elapsed_time


    jitter = 0.05

    # Scatter plots
    plt.scatter([1] * num + np.random.normal(0, jitter, num), elapsed_time1, s=10, color='red', label='sha1')
    plt.scatter([2] * num + np.random.normal(0, jitter, num), elapsed_time2, s=10, color='blue', label='sha256')
    plt.scatter([3] * num + np.random.normal(0, jitter, num), elapsed_time3, s=10, color='green', label='sha512')

    # Labels and legend
    plt.xlabel('index')
    plt.ylabel('elapsed_time')
    plt.legend()

    plt.savefig('algorithm.png')
    plt.clf()



    # Scatter plots
    plt.scatter([0] * num + np.random.normal(0, jitter, num), time_, s=10, color='black', label='plain text')
    plt.scatter([1] * num + np.random.normal(0, jitter, num), elapsed_time1, s=10, color='red', label='sha1')
    plt.scatter([2] * num + np.random.normal(0, jitter, num), elapsed_time2, s=10, color='blue', label='sha256')
    plt.scatter([3] * num + np.random.normal(0, jitter, num), elapsed_time3, s=10, color='green', label='sha512')

    # Labels and legend
    plt.xlabel('index')
    plt.ylabel('elapsed_time')
    plt.legend()

    plt.savefig('algorithm_with_plain.png')
    plt.clf()