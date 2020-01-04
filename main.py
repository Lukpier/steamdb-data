from steamdb.steam_db_service import SteamDBService
import json

if __name__ == "__main__":
    service = SteamDBService()
    histories = service.collectLastWeekPlayerHistories()
    with open('players_histories.json', 'w') as f:
        json.dump(histories, f)
