from typing import List, Optional
from uuid import uuid4

import chromadb
from chromadb.api.types import IncludeEnum
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from xraygpt.db.base import Database, Item

SPLITTER = "|"


class ChromaDatabase(Database):
    def __init__(self, ebd: OpenAIEmbeddings, path: Optional[str] = None):
        self.ebd = ebd
        if path is not None:
            client = chromadb.PersistentClient(path=path)
        else:
            client = chromadb.Client()
        self.collection = client.get_or_create_collection("people")

    def add(self, item: Item):
        keys = SPLITTER.join(item["name"])
        logger.trace("Adding item {name} with id {id}", name=keys, id=item["id"])
        embedding = self.ebd.embed_query(item["description"])
        self.collection.add(
            documents=[item["description"]],
            embeddings=[embedding],  # type: ignore[arg-type]
            metadatas=[{"keys": keys, "frequency": item["frequency"]}],
            ids=[item["id"]],
        )

    def delete(self, item: Item):
        logger.trace("Deleting item with id {id}", id=item["id"])
        self.collection.delete(ids=[item["id"]])

    def query(self, name: str, n=3) -> List[Item]:
        embedding = self.ebd.embed_query(name)
        results = self.collection.query(embedding, n_results=n)

        return [
            Item(
                id=ix,
                name=meta["keys"].split(SPLITTER),
                description=doc,
                frequency=meta["frequency"],
            )
            for ix, doc, meta in zip(
                results["ids"][0], results["documents"][0], results["metadatas"][0]  # type: ignore[index]
            )
        ]

    def dump(self) -> List[Item]:
        results = self.collection.get(
            include=[IncludeEnum.metadatas, IncludeEnum.documents]
        )
        data = [
            Item(
                id=ix,
                name=meta["keys"].split(SPLITTER),  # type: ignore[union-attr]
                description=doc,
                frequency=meta["frequency"],  # type: ignore[typeddict-item]
            )
            for ix, doc, meta in zip(
                results["ids"], results["documents"], results["metadatas"]  # type: ignore[arg-type]
            )
        ]
        return sorted(data, key=lambda x: x["frequency"], reverse=True)
