import os
import sys
from multiprocessing import Process
from steamdb.apps.apps_importer import AppsImporter
from steamdb.players.players_history_importer import PlayersHistoryImporter
from steamdb.prices.prices_history_importer import PricesHistoryImporter
from db.file_db import JsonFileDB

if os.path.exists(os.path.join("steamdb", "apps", "apps_importer.py")):
    # we are running this from a local checkout
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

if __name__ == "__main__":
    db = JsonFileDB() # todo: parametrize
    apps_importer = AppsImporter(db)
    players_importer = PlayersHistoryImporter(db)
    prices_importer = PricesHistoryImporter(db)
    
    apps_importer.ingest()

    runInParallel(players_importer.ingest, prices_importer.ingest)
    
