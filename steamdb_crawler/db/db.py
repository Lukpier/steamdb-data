from abc import ABC, abstractmethod

###
# Abstract class for a data lake. two main methods should be extended in child classes. 
# raw read and raw write. usefull to ingest large amount of data to be later used in any business logic application.
###
class DataLake(ABC):

    @abstractmethod
    def write(self, records: list, table: str) -> bool:
        pass

    @abstractmethod
    def read(self, table: str) -> list:
        pass
