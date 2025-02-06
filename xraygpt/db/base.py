from abc import abstractmethod
from typing import List, TypedDict


class Item(TypedDict):
    id: str
    name: List[str]
    description: str
    frequency: int


class Database:
    @abstractmethod
    def add(self, item: Item) -> None:
        pass

    @abstractmethod
    def delete(self, item: Item) -> None:
        pass

    @abstractmethod
    def query(self, name: str) -> List[Item]:
        pass

    @abstractmethod
    def dump(self) -> List[Item]:
        pass
