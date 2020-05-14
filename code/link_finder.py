from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):

    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.links = set()

    # Finds all the non-email hyperlinks in the html page
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        for (attribute, value) in attrs:
            if attribute != 'href' :
                continue
            link = parse.urljoin(self.base_url, value)    
            if 'mailto' not in link:
                self.links.add((link, self.page_url))
        
    # returns hyperlinks found in a page
    def get_page_links(self):
        return self.links
