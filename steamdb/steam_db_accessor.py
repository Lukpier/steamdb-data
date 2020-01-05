from common.requests_api import RequestsApi
from steamdb.query_mode import QueryMode
app_id = "292030" # the witcher 3 app id on steam
import json
import random
import os
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

class SteamDBAccessor:
    def __init__(self):
        self.appIdsAccessor = RequestsApi('api.steampowered.com')
        self.dataAccessor = RequestsApi('steamdb.info')
        self.dataAccessorHeaders = {
            'Accept': 'application/json',
            'Referer': 'https://steamdb.info/'
        }
        with open('steamdb/user_agents.json') as f:
            self.user_agents = json.load(f)

    def getAppIds(self):
        app_ids_data = self.appIdsAccessor.get('/ISteamApps/GetAppList/v2/', headers=self.dataAccessorHeaders)
        return json.loads(app_ids_data)

    def getPlayersHistory(self, app_id: str, mode: QueryMode) -> dict:
        _type = "concurrent_week" if (mode == QueryMode.WEEKLY) else "concurrent_max"
        service_url = '/api/GetGraph/?type={}&appid={}'.format(_type, app_id)
        headers = self.randomUserAgentToHeaders(self.user_agents)
        r = self.dataAccessor.get(service_url, headers = headers)
        try:
            return json.loads(r)
        except json.decoder.JSONDecodeError:
            # try with a different user-agent (some may cause problems)
            # remove user agent
            logger.info('Encountered problems which may have been caused by wrong user agent. removing it from list')
            logger.info('trying again')
            self.user_agents.remove(headers['User-Agent'])
            return self.getPlayersHistory(app_id, mode)

    def getPricesHistory(self, app_id: str, currency="eu") -> dict:
        service_url = '/api/GetPriceHistory/?appid={}&cc={}'.format(app_id, currency)
        r = self.dataAccessor.get(service_url, headers = self.dataAccessorHeaders)
        return json.loads(r)
    
    def randomUserAgentToHeaders(self, user_agent_list: list) -> dict:
        user_agent = random.choice(user_agent_list)
        headers = self.dataAccessorHeaders
        headers['User-Agent'] = user_agent
        return headers

