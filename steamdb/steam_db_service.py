from steamdb.steam_db_accessor import SteamDBAccessor
from steamdb.query_mode import QueryMode
import logging

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

class SteamDBService:

    def __init__(self):
        self.accessor = SteamDBAccessor()
    
    def collectLastWeekPlayerHistories(self):
        logger.info('Retrieving all app ids from steam api...')
        apps = self.accessor.getAppIds()['applist']['apps']
        logger.info('Done. Start collecting players history for %s apps', len(apps))
        res = []
        for app in apps:
            r = {}
            name = app['name']
            _id = app['appid']
            logger.info('Querying steam db api for %s', name)
            history = self.accessor.getPlayersHistory(_id, QueryMode.WEEKLY)
            if (history['success']):
                r['app_name'] = name
                r['app_id'] = _id
                r['players_history'] = history['data']
                res.append(r)
            else: 
                logger.info('No players history data for %s', name)
        return res
