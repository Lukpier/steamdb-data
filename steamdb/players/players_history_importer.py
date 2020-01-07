from steamdb.players.players_history_service import PlayersHistoryService
from db.db import DataLake
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class PlayersHistoryImporter:

    def __init__(self, db: DataLake):
        self.service = PlayersHistoryService()
        self.db = db

    def start(self, app_numbers: int = None):
        logger.info('reading app ids list from db..')
        apps = self.db.read('steam_apps')
        if (app_numbers is not None):
            apps = apps[:app_numbers]
        player_histories = self.service.getPlayersHistories(apps)
        self.db.write(player_histories, 'players_histories')