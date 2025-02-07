from copy import deepcopy
from typing import List

from loguru import logger

from xraygpt.db.base import Database, Item


class TextCache(Database):
    def __init__(self, db: Database):
        self.db = db
        self.item_cache = {}
        self.name_cache = {}

        for i in self.db.dump():
            self._add_cache(i)

    def add(self, item: Item) -> None:
        self._add_cache(item)
        return self.db.add(item)

    def delete(self, item: Item) -> None:
        self._delete_cache(item)
        return self.db.delete(item)

    def query(self, name: str, n=3) -> List[Item]:
        name_item = self._query_cache(name)
        db_item = self.db.query(name, n)

        name_id = [i["id"] for i in name_item]
        db_id = [i["id"] for i in db_item]
        both_item = [i for i in db_item if i["id"] in name_id]
        db_only_item = [i for i in db_item if i["id"] not in name_id]
        name_only_item = [i for i in name_item if i["id"] not in db_id]

        # date count may exceed n, but it's fine for now
        return both_item + name_only_item + db_only_item

    def dump(self) -> List[Item]:
        return self.db.dump()

    def _add_cache(self, item: Item) -> None:
        self.item_cache[item["id"]] = deepcopy(item)
        for i in item["name"]:
            if i not in self.name_cache or self.name_cache[i] is None:
                self.name_cache[i] = [item["id"]]
            elif item["id"] in self.name_cache[i]:
                logger.warning("Duplicate name found in cache: {name}", name=i)
                self.name_cache[i].append(item["id"])
            else:
                logger.warning("Duplicate item found in cache name {name}", name=i)

    def _delete_cache(self, item: Item) -> None:
        del self.item_cache[item["id"]]
        for i in item["name"]:
            # name_cache many contain duplicate id
            self.name_cache[i] = [j for j in self.name_cache.get(i, []) if j != item["id"]]
            if len(self.name_cache[i]) == 0:
                del self.name_cache[i]

    def _query_cache(self, name: str) -> List[Item]:
        if name in self.name_cache:
            return [self.item_cache[i] for i in self.name_cache[name]]
        return []
