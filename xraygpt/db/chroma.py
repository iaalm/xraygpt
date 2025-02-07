from typing import List, Optional
from uuid import uuid4

import chromadb
from langchain_openai import OpenAIEmbeddings
from loguru import logger

from xraygpt.db.base import Database, Item

SPLITTER = "|"


class ChromaDatabase(Database):
    def __init__(self, llm: Optional[OpenAIEmbeddings], path: Optional[str] = None):
        self.llm = llm
        if path is not None:
            client = chromadb.PersistentClient(path=path)
        else:
            client = chromadb.Client()
        self.collection = client.get_or_create_collection("people")

    def add(self, item: Item):
        if self.llm is None:
            raise ValueError("LLM is not set")
        keys = SPLITTER.join(item["name"])
        logger.trace("Adding item {name} with id {id}", name=keys, id=item["id"])
        embedding = self.llm.embed_query(item["description"])
        self.collection.add(
            documents=[item["description"]],
            embeddings=[embedding],
            metadatas=[{"keys": keys, "frequency": item["frequency"]}],
            ids=[item["id"]],
        )

    def delete(self, item: Item):
        logger.trace("Deleting item with id {id}", id=item["id"])
        self.collection.delete(ids=[item["id"]])

    def query(self, name: str, n=3) -> List[Item]:
        if self.llm is None:
            raise ValueError("LLM is not set")
        embedding = self.llm.embed_query(name)
        results = self.collection.query(embedding, n_results=n)
        return [
            Item(
                id=ix,
                name=meta["keys"].split(SPLITTER),
                description=doc,
                frequency=meta["frequency"],
            )
            for ix, doc, meta in zip(
                results["ids"][0], results["documents"][0], results["metadatas"][0]
            )
        ]

    def dump(self) -> List[Item]:
        results = self.collection.get(include=["documents", "metadatas"])
        data = [
            Item(
                id=ix,
                name=meta["keys"].split(SPLITTER),
                description=doc,
                frequency=meta["frequency"],
            )
            for ix, doc, meta in zip(
                results["ids"], results["documents"], results["metadatas"]
            )
        ]
        return sorted(data, key=lambda x: x["frequency"], reverse=True)
