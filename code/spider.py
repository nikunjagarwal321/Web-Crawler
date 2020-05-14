import db_operations
import domain
from link_finder import LinkFinder
from urllib.error import HTTPError
from urllib.request import urlopen


class Spider:
    
    sub_domain_name = ''
    base_url = ''
    queue_table = 'queued_links'
    crawled_table = 'crawled_links'
    error_table = 'error_links'
    foreign_table = 'foreign_links'
    queued_links = set()
    crawled_links = set()
    error_links = set()
    foreign_links = set()

    def __init__(self, base_url):
        Spider.base_url = base_url
        Spider.sub_domain_name = domain.get_sub_domain_name(base_url)
        self.boot()
        # self.handle_robots_file()
        self.queued_links.add((Spider.base_url, ""))
        self.crawl_page('Spider 1', (Spider.base_url, ""))

    # Create database
    @staticmethod
    def boot():
        db_operations.create_database()
        Spider.queued_links = db_operations.retrieve_links_from_db(Spider.queue_table)
        Spider.crawled_links = db_operations.retrieve_links_from_db(Spider.crawled_table)
        Spider.error_links = db_operations.retrieve_links_from_db(Spider.error_table)
        Spider.foreign_links = db_operations.retrieve_links_from_db(Spider.foreign_table)

    # Crawl webpages
    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled_links:
            print(thread_name + ' is crawling ' + page_url[0])
            print('Queue ' + str(len(Spider.queued_links)) + ' | Crawled ' + str(len(Spider.crawled_links)))
            links  = Spider.gather_links(page_url)
            Spider.add_links_to_queue(links)
            Spider.queued_links.remove(page_url)
            Spider.crawled_links.add(page_url)
            Spider.update_files()

    # Open a webpage and gather links from it
    @staticmethod
    def gather_links(page_url):
        parent_link = page_url[1]
        curr_link = page_url[0]
        html_string = ''
        try:
            response = urlopen(curr_link)
            if 'text/html' in response.getheader('Content-Type') :
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            link_finder = LinkFinder(Spider.base_url, curr_link)
            link_finder.feed(html_string)
        except HTTPError as e:
            Spider.error_links.add((curr_link, parent_link, e.code, Spider.check_url_type(curr_link)))
            print(e)
            return set()
        return link_finder.get_page_links()

    # Add new hyperlinks to current queue
    @staticmethod
    def add_links_to_queue(urls):
        for url in urls:
            parent_link = url[1]
            curr_link = url[0]
            if curr_link in Spider.crawled_links:
                continue
            if curr_link in Spider.queued_links:
                continue
            if Spider.sub_domain_name not in curr_link:
                Spider.foreign_links.add((curr_link, parent_link, Spider.check_url_type(curr_link)))
            Spider.queued_links.add(url)
    
    # Returns type of url
    @staticmethod
    def check_url_type(url):
        if Spider.sub_domain_name not in url:
             if "amazon.com" in domain.get_domain_name(url):
                return 'all-amazon'
             else:
                return 'non-amazon'
        return 'dev-amazon'


    # Transfer sets to database
    @staticmethod
    def update_files():
        db_operations.insert_links_to_db(Spider.queue_table, Spider.queued_links)
        db_operations.insert_links_to_db(Spider.crawled_table, Spider.crawled_links)
        db_operations.insert_links_to_db(Spider.error_table, Spider.error_links)
        db_operations.insert_links_to_db(Spider.foreign_table, Spider.foreign_links)
