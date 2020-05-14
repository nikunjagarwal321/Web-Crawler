# to find status code

from urllib.error import HTTPError
from urllib.request import urlopen

try:
    response = urlopen("https://developer.amazon.com/alexa-auto/design-toolkit.html")
    print(response.getcode())
except HTTPError as e:
    print(e.code)
    
