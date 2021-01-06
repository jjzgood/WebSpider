import requests
import logging
import time
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s: %(message)s')

TOTAL_NUMBER = 10
BASE_URL = 'https://static4.scrape.cuiqingcai.com/detail/{id}'

start_time = time.time()

for id in range(1, TOTAL_NUMBER + 1):
   url = BASE_URL.format(id=id)
   logging.info('scraping %s', url)
   response = requests.get(url,verify=False)
   print('Get response from', url, 'response', response)

end_time = time.time()
logging.info('total time %s seconds', end_time - start_time)
# total time 137.63853311538696 seconds
