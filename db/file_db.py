from db.db import DataLake
import json
import logging

logger = logging.getLogger(__name__)

class JsonFileDB(DataLake):

    def write(self, records: list, table: str):
        with open('output/datalake/{}.json'.format(table), 'w') as f:
            json.dump(records, f)

    def read(self, table) -> dict:
        with open('output/datalake/{}.json'.format(table)) as f:
            return json.load(f)
