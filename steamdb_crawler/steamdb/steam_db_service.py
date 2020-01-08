from steamdb.steam_db_accessor import SteamDBAccessor
from steamdb.query_mode import QueryMode
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

batch = 900
seconds_to_wait = 60

class SteamDBService:

    def __init__(self):
        self.accessor = SteamDBAccessor()

    def retrieveData(self, apps: list, what) -> list:
        if what == 'players':
            return self.getDataForApps(apps, self.accessor.getPlayersHistory)
        elif what == 'prices':
            return self.getDataForApps(apps, self.accessor.getPricesHistory)

        
    def getDataForApps(self, apps: list, queryFn) -> list:
        res = []
        for i, app in enumerate(apps):
            name = app['name']
            _id = app['appid']
            logger.info('Querying steam db api for %s', name)
            history = self.getDataForApp(_id, name, queryFn)
            res.append(history)
            if (i != 0) and (i % batch) == 0:
                logger.info('Waiting %i seconds to prevent crawl..', seconds_to_wait)
                time.sleep(seconds_to_wait)
            else:
                time.sleep(0.05)
        return res

    def getDataForApp(self, app_id: str, app_name: str, queryFn) -> dict:
        history = queryFn(app_id)
        if (history['success']):
            return self.mkRes(app_id, app_name, history['data'])
        elif (history.get('error') is not None and 'crawl' in history['error']):
            logger.info('SteamDB temporary blocked us. waiting %i seconds, then try again', seconds_to_wait)
            time.sleep(seconds_to_wait)
            return self.getDataForApp(app_id, app_name, queryFn)
        else: 
            logger.info('No players history data for %s', app_name)
            return self.mkRes(app_id, app_name, {})

    def mkRes(self, app_id: str, app_name: str, history: dict):
        r = {}
        r['app_name'] = app_name
        r['app_id'] = app_id
        r['players_history'] = history
        return r
