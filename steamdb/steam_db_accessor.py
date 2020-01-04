from common.requests_api import RequestsApi
from steamdb.query_mode import QueryMode
app_id = "292030" # the witcher 3 app id on steam
import json

class SteamDBAccessor:
    def __init__(self):
        self.appIdsAccessor = RequestsApi('api.steampowered.com')
        self.dataAccessor = RequestsApi('steamdb.info')
        self.dataAccessorHeaders = {
            'Accept': 'application/json',
            'Referer': 'https://steamdb.info/',
        }

    def getAppIds(self):
        app_ids_data = self.appIdsAccessor.get('/ISteamApps/GetAppList/v2/', headers=self.dataAccessorHeaders)
        return json.loads(app_ids_data)

    def getPlayersHistory(self, app_id: str, mode: QueryMode) -> dict:
        _type = "concurrent_week" if (mode == QueryMode.WEEKLY) else "concurrent_max"
        service_url = '/api/GetGraph/?type={}&appid={}'.format(_type, app_id)
        r = self.dataAccessor.get(service_url, headers = self.dataAccessorHeaders)
        return json.loads(r)

    def getPricesHistory(self, app_id: str, currency="eu") -> dict:
        service_url = '/api/GetPriceHistory/?appid={}&cc={}'.format(app_id, currency)
        r = self.dataAccessor.get(service_url, headers = self.dataAccessorHeaders)
        return json.loads(r)

