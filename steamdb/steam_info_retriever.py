from common.requests_api import RequestsApi
from steamdb.query_mode import QueryMode
app_id = "292030" # the witcher 3 app id on steam

class SteamDBAccessor:
    def __init__(self):
        self.client = RequestsApi('steamdb.info')
        self.headers = {
            'Accept': 'application/json',
            'Referer': 'https://steamdb.info/',
        }
    
    def getPlayers(self, app_id: str, mode: QueryMode) -> dict:
        _type = "concurrent_week" if (mode == QueryMode.WEEKLY) else "concurrent_max"
        service_url = '/api/GetGraph/?type={}&appid={}'.format(_type, app_id)
        r = self.client.get(service_url, headers = self.headers)
        print(r)

    def getPrices(self, app_id: str, currency="eu") -> dict:
        service_url = '/api/GetPriceHistory/?appid={}&cc={}'.format(app_id, currency)
        r = self.client.get(service_url, headers = self.headers)
        print(r)

