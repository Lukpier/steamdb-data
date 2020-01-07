from db.db import DataLake
from db.file_db import JsonFileDB
from steamdb.steam_db_accessor import SteamDBAccessor
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class AppsImporter:

    def __init__(self, db: DataLake):
        self.accessor = SteamDBAccessor() 
        self.db = db

    def start(self):
        logger.info('Retrieving all app ids from steam api...')
        apps = self.accessor.getAppIds()
        apps = apps['applist']['apps']
        logger.info('Writing %i  to db', len(apps))
        self.db.write(apps, 'steam_apps')
        logger.info('Done.')


def start(db_type = 'file'):
    if db_type == 'file':
        db = JsonFileDB()
        importer = AppsImporter(db)
        importer.start()

start()
