import http.client
import mimetypes

class RequestsApi:
    def __init__(self, base_url, **kwargs):
        self.connection =  http.client.HTTPSConnection(base_url)

    def get(self, url, **kwargs):
        self.connection.request("GET", url, **kwargs)
        res = self.connection.getresponse()
        data = res.read()
        return data.decode("utf-8")