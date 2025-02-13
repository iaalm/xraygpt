import hashlib
import os
import sqlite3
from typing import Optional

from loguru import logger

from xraygpt.xraydb.init_script import X_RAY_DB_INIT_SCRIPT
from xraygpt.xraydb.types import Entity, Language, Table


def _hashAsin(filename: str) -> str:
    basename = os.path.basename(filename)
    print(basename)
    return (
        "BB"
        + hashlib.sha3_224(basename[: basename.rindex(".")].encode()).hexdigest()[:8]
    )


class XRayDb:
    def __init__(
        self,
        base_filename: str,
        asin: Optional[str] = None,
        language: Language = Language.EN,
    ):
        self.root = base_filename[: base_filename.rindex(".")] + ".sdr"
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        self.asin = asin if asin is not None else _hashAsin(base_filename)
        self.language = language
        db_filename = f"{self.root}/XRAY.entities.{self.asin}.asc"
        if not os.path.exists(db_filename):
            to_init = True
        else:
            to_init = False
        self.db = sqlite3.connect(db_filename)
        if to_init:
            self.init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.db.commit()
        self.db.close()

    def init_db(self):
        logger.info("Initializing X-Ray database")
        self.db.executescript(X_RAY_DB_INIT_SCRIPT)

    def _get_next_id(self, table_name: str) -> int:
        cursor = self.db.cursor()
        cursor.execute(f"SELECT MAX(id) FROM {table_name};")
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 0

    def add_entity(self, entity: Entity) -> int:
        entity_id = self._get_next_id(Table.ENTITY)
        self.db.execute(
            "INSERT INTO entity(id, label, type, count, has_info_card ) VALUES (?, ?, ?, ?, ?);",
            (entity_id, entity["name"], entity["type"], entity["count"], 1),
        )
        self.db.execute(
            "INSERT INTO entity_description(text, source_wildcard, source, entity) VALUES (?, ?, ?, ?);",
            (entity["description"], entity["name"], entity["source"], entity_id),
        )

        return entity_id
