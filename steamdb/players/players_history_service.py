from steamdb.steam_db_accessor import SteamDBAccessor
from steamdb.query_mode import QueryMode
import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

batch = 900
seconds_to_wait = 60

class PlayersHistoryService:

    def __init__(self):
        self.accessor = SteamDBAccessor()
        
    def getPlayersHistories(self, apps: list) -> list:
        res = []
        for i, app in enumerate(apps):
            name = app['name']
            _id = app['appid']
            logger.info('Querying steam db api for %s', name)
            self.getPlayersHistory(_id, name)
            print(i)
            if (i != 0) and (i % batch) == 0:
                logger.info('Waiting %i seconds to prevent crawl..', seconds_to_wait)
                time.sleep(seconds_to_wait)
            else:
                time.sleep(0.05)
        return res

    def getPlayersHistory(self, app_id: str, app_name: str) -> dict:
        history = self.accessor.getPlayersHistory(app_id, QueryMode.FULL)
        if (history['success']):
            return self.mkRes(app_id, app_name, history)
        elif (history.get('error') is not None and 'crawl' in history['error']):
            logger.info('SteamDB temporary blocked us. waiting %i seconds, then try again', seconds_to_wait)
            time.sleep(seconds_to_wait)
            return self.getPlayersHistory(app_id, app_name)
        else: 
            logger.info('No players history data for %s', app_name)
            return {}

    def mkRes(self, app_id: str, app_name: str, history: dict):
        r = {}
        r['app_name'] = app_name
        r['app_id'] = app_id
        r['players_history'] = history['data']
        return r
