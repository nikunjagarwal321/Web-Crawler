import db_operations
import threading
from queue import Queue
from spider import Spider
from time import sleep



HOMEPAGE = 'https://developer.amazon.com/documentation'
QUEUE_TABLE = 'queued_links'
CRAWLED_TABLE = 'crawled_links'
NUMBER_OF_THREADS = 1
queue = Queue()
Spider(HOMEPAGE)

# continue creating more jobs if Queue file is not empty
def crawl():
    queued_links = db_operations.retrieve_links_from_db(QUEUE_TABLE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue ')
        create_jobs()

# add links to queue
def create_jobs():
    for link in db_operations.retrieve_links_from_db(QUEUE_TABLE):
        queue.put(link)
    # wait on the queue until everything has been processed  
    queue.join()
    crawl()


# make a pool of threads and give work to them
def create_spiders():
    for i in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=work)
        thread.daemon = True
        thread.start()

# work is to pop a link and crawl it
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        
        queue.task_done()


create_spiders()
crawl()