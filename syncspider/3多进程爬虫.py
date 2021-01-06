import requests
import logging
import time
from multiprocessing import Pool
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s: %(message)s')


def request(page):
    url = 'https://static4.scrape.cuiqingcai.com/detail/{id}'.format(id=page)
    logging.info('scraping %s', url)
    response = requests.get(url, verify=False)
    print('Get response from', url, 'response', response)

if __name__ == '__main__':

    start_time = time.time()
    pool = Pool(10)
    pool.map(request,range(1,11))
    pool.close()

    end_time = time.time()
    logging.info('total time %s seconds', end_time - start_time)

# total time 52.55535316467285 seconds