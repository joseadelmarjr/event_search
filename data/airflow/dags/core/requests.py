import requests

class RequestApi:
    def __init__(self):
        pass
    
    def get_endpoint(self, url, header = {}):
        if not header:
            request = requests.get(url)
            return request 
            
