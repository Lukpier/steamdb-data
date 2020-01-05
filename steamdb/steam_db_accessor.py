from common.requests_api import RequestsApi
from steamdb.query_mode import QueryMode
app_id = "292030" # the witcher 3 app id on steam
import json
import random

user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
  ]

class SteamDBAccessor:
    def __init__(self):
        self.appIdsAccessor = RequestsApi('api.steampowered.com')
        self.dataAccessor = RequestsApi('steamdb.info')
        self.dataAccessorHeaders = {
            'Accept': 'application/json',
            'Referer': 'https://steamdb.info/'
        }

    def getAppIds(self):
        app_ids_data = self.appIdsAccessor.get('/ISteamApps/GetAppList/v2/', headers=self.dataAccessorHeaders)
        return json.loads(app_ids_data)

    def getPlayersHistory(self, app_id: str, mode: QueryMode) -> dict:
        _type = "concurrent_week" if (mode == QueryMode.WEEKLY) else "concurrent_max"
        service_url = '/api/GetGraph/?type={}&appid={}'.format(_type, app_id)
        r = self.dataAccessor.get(service_url, headers = self.randomUserAgentToHeaders(user_agent_list))
        print(r)
        return json.loads(r)

    def getPricesHistory(self, app_id: str, currency="eu") -> dict:
        service_url = '/api/GetPriceHistory/?appid={}&cc={}'.format(app_id, currency)
        r = self.dataAccessor.get(service_url, headers = self.dataAccessorHeaders)
        return json.loads(r)
    
    def randomUserAgentToHeaders(self, user_agent_list: list) -> dict:
        user_agent = random.choice(user_agent_list)
        headers = self.dataAccessorHeaders
        headers['User-Agent'] = user_agent
        return headers

