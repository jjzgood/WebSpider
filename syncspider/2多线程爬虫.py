import requests
import logging
import time
import threading
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s: %(message)s')


def request(page):
    url = 'https://static4.scrape.cuiqingcai.com/detail/{id}'.format(id=page)
    logging.info('scraping %s', url)
    response = requests.get(url, verify=False)
    print('Get response from', url, 'response', response)

start_time = time.time()

threads = []
for i in range(1,11):
    task = threading.Thread(target=request,args=(i,))
    threads.append(task)
    task.start()

for thread in threads:
    thread.join()

end_time = time.time()
logging.info('total time %s seconds', end_time - start_time)
# total time 137.63853311538696 seconds