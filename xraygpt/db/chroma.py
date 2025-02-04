from typing import List
from uuid import uuid4
from langchain_openai import OpenAIEmbeddings
import chromadb
from xraygpt.db.base import Database, Item

SPLITTER = "|"

class ChromaDatabase(Database):
    def __init__(self, llm: OpenAIEmbeddings):
        self.llm = llm
        client = chromadb.Client()
        self.collection = client.create_collection("people")

    def add(self, item: Item):
        new_id = uuid4().hex
        keys = SPLITTER.join(item["name"])
        embedding = self.llm.embed_query(item["description"])
        self.collection.add(
            documents=[item["description"]],
            embeddings=[embedding],
            metadatas=[{"keys": keys}],
            ids=[item["id"]],
        )

    def delete(self, item: Item):
        self.collection.delete(ids=[item["id"]])

    def query(self, name: str, n=3) -> List[Item]:
        embedding = self.llm.embed_query(name)
        results = self.collection.query(embedding, n_results=n)
        return [Item(id=ix, name=meta["keys"].split(SPLITTER), description=doc) for ix, doc, meta in zip(results["ids"], results["documents"][0], results["metadatas"][0])]


