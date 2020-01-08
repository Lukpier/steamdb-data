import os
import sys
from steamdb.apps.apps_importer import AppsImporter
from steamdb.players.players_history_importer import PlayersHistoryImporter
from db.file_db import JsonFileDB

if os.path.exists(os.path.join("steamdb", "apps", "apps_importer.py")):
    # we are running this from a local checkout
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))


if __name__ == "__main__":
    db = JsonFileDB() # todo: parametrize
    apps_importer = AppsImporter(db)
    players_importer = PlayersHistoryImporter(db)
    apps_importer.ingest()
    players_importer.ingest()
    
