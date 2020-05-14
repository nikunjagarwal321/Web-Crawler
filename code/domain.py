from urllib.parse import urlparse

# get domain name 
def get_domain_name(url):
    try:
        sub_domain = get_sub_domain_name(url).split('.')
        return sub_domain[-2] + '.' + sub_domain[-1]
    except:
        return ''
        
# get sub-domain name 
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

