import logging
import json
from pyppeteer import launch
from pyppeteer.errors import TimeoutError,ElementHandleError
import asyncio
from os import makedirs
from os.path import exists

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s: %(message)s')
BASE_URL = 'https://read.douban.com'
INDEX_URL = 'https://read.douban.com/category?page={page}&kind=104'
TIMEOUT = 10
TOTAL_PAGE = 20
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 1366
HEADLESS = False
RESULTS_DIR = 'results'


async def init():
    global browser,tab
    browser = await launch(headless=HEADLESS, args=['--disable-infobars', f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})


async def scrape_page(url,selector):
    logging.info('scraping %s',url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector,options={
            'timeout':TIMEOUT*1000
        })
    except TimeoutError:
        logging.error('error occurred while scraping %s',url,exc_info=True)


async def scrape_index(page):
    url = INDEX_URL.format(page=page)
    await scrape_page(url,'.works-list .works-item')
    await asyncio.sleep(2)


async def parse_index():
    return await tab.querySelectorAllEval('.works-list .works-item', 'nodes => nodes.map(node => node.getAttribute("href"))')


async def scrape_detail(url):
    await scrape_page(url,'h1')


async def parse_detail():
    url = tab.url
    name = await tab.querySelectorEval('h1','node => node.innerText')
    author = await tab.querySelectorEval('.author .labeled-text', 'node => node.innerText')
    try:
        score = await tab.querySelectorEval('.score', 'node => node.innerText')
    except ElementHandleError:
        score = 0
    try:
        about = await tab.querySelectorEval('.abstract-full .info', 'node => node.innerText')
    except ElementHandleError:
        # 套装
        about = await tab.querySelectorAllEval('.bd p', 'nodes => nodes.map(node => node.innerText)')
    return {
        'url': url,
        'name': name,
        'author': author,
        'score': score,
        'about': about
    }


exists(RESULTS_DIR) or makedirs(RESULTS_DIR)
async def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


async def main():
   await init()
   try:
       for page in range(1, TOTAL_PAGE + 1):
           await scrape_index(page)
           detail_urls = await parse_index()
           for detail_url in detail_urls:
               await scrape_detail(BASE_URL+detail_url)
               detail_data = await parse_detail()
               await save_data(detail_data)
               logging.info('save data %s', detail_data)
   finally:
       await browser.close()

if __name__ == '__main__':
   asyncio.get_event_loop().run_until_complete(main())