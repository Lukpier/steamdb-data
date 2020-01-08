from steamdb.steam_db_service import SteamDBService
from db.db import DataLake
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class PricesHistoryImporter:

    def __init__(self, db: DataLake):
        self.service = SteamDBService()
        self.db = db

    def ingest(self, app_numbers: int = None):
        logger.info('reading app ids list from db..')
        apps = self.db.read('steam_apps')
        if (app_numbers is not None):
            apps = apps[:app_numbers]
        player_histories = self.service.retrieveData(apps, 'prices')
        self.db.write(player_histories, 'prices_histories')
        logger.info('Done.')