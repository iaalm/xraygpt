from typing import List, Optional
from uuid import uuid4

import chromadb
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from xraygpt.db.base import Database, Item

SPLITTER = "|"


class ChromaDatabase(Database):
    def __init__(self, llm: OpenAIEmbeddings, path: Optional[str] = None):
        self.llm = llm
        if path is not None:
            client = chromadb.PersistentClient(path=path)
        else:
            client = chromadb.Client()
        self.collection = client.get_or_create_collection("people")

    def add(self, item: Item):
        new_id = uuid4().hex
        keys = SPLITTER.join(item["name"])
        logger.info("Adding item {name} with id {id}", name=keys, id=new_id)
        embedding = self.llm.embed_query(item["description"])
        self.collection.add(
            documents=[item["description"]],
            embeddings=[embedding],
            metadatas=[{"keys": keys}],
            ids=[new_id],
        )

    def delete(self, item: Item):
        logger.info("Deleting item with id {id}", id=item["id"])
        self.collection.delete(ids=[item["id"]])

    def query(self, name: str, n=3) -> List[Item]:
        embedding = self.llm.embed_query(name)
        results = self.collection.query(embedding, n_results=n)
        return [
            Item(id=ix, name=meta["keys"].split(SPLITTER), description=doc)
            for ix, doc, meta in zip(
                results["ids"][0], results["documents"][0], results["metadatas"][0]
            )
        ]

    def dump(self) -> List[Item]:
        results = self.collection.get(include=["documents", "metadatas"])
        return [
            Item(id=ix, name=meta["keys"].split(SPLITTER), description=doc)
            for ix, doc, meta in zip(
                results["ids"], results["documents"], results["metadatas"]
            )
        ]
