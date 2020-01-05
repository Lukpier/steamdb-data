from steamdb.steam_db_accessor import SteamDBAccessor
from steamdb.query_mode import QueryMode
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

concurrent = 200
batch = 900

class SteamDBService:

    def __init__(self):
        self.accessor = SteamDBAccessor()
    
    def collectLastWeekPlayerHistories(self):
        logger.info('Retrieving all app ids from steam api...')
        apps = self.accessor.getAppIds()['applist']['apps']
        logger.info('Done. Start collecting players history for %s apps', len(apps))
        return self.getPlayersHistories(apps)

    def getPlayersHistories(self, apps: list) -> list:
        res = []
        for i, app in enumerate(apps):
            name = app['name']
            _id = app['appid']
            logger.info('Querying steam db api for %s', name)
            self.getPlayersHistory(_id, name)
            print(i)
            if (i != 0) and (i % 900) == 0:
                logger.info('Waiting 10 seconds to prevent crawl..')
                time.sleep(30)
            else:
                time.sleep(0.05)
        return res

    def getPlayersHistory(self, app_id: str, app_name: str) -> dict:
        history = self.accessor.getPlayersHistory(app_id, QueryMode.FULL)
        if (history['success']):
            return self.mkRes(app_id, app_name, history)
        else: 
            logger.info('No players history data for %s', app_name)
            return {}

    def mkRes(self, app_id: str, app_name: str, history: dict):
        r = {}
        r['app_name'] = app_name
        r['app_id'] = app_id
        r['players_history'] = history['data']
        return r
