import asyncio
import json

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_openai.chat_models.base import BaseChatOpenAI

from xraygpt.db.base import Database
from xraygpt.db.chroma import ChromaDatabase
from xraygpt.xraydb import Entity, EntitySource, EntityType, XRayDb


def dumpDatabese(filename: str, db: Database):
    json_filename = filename[: filename.rindex(".")] + ".json"
    data = db.dump()
    # [ [name, type, alias, description, source, omit], ...]

    # item only occurs in one chapter is not necessary to add,
    # This also helps to filter out celebrity's names.
    characters = [
        (
            i["name"][0],
            "PERSON",
            ",".join(i["name"][1:]),
            i["description"],
            None,
            i["frequency"] <= 1,
        )
        for i in data
    ]

    with open(json_filename, "w") as fp:
        json.dump(
            characters,
            fp,
            indent=4,
            ensure_ascii=False,
        )


def dumpDatabese_x_ray_creater(filename: str, db: Database):
    json_filename = filename[: filename.rindex(".")] + ".json"
    data = db.dump()
    # {"characters":	{"Character1 Name":	{"description": "Character1 Description",
    #               		     "aliases": ["Character1 Alias1", ...]},
    #                    "Character2 Name":	{"description": "Character2 Description",
    #               		     "aliases": ["Character1 Alias2", ...]},
    #  ...},
    # "settings": 	{"Setting1 Name":	{"description": "Setting1 Description",
    #                       		    "aliases": ["Setting1 Alias1", ...]}
    #  ...},
    # "quotes":	["Quote1",
    #         	 "Quote2",
    #  ...]}

    # item only occurs in one chapter is not necessary to add,
    # This also helps to filter out celebrity's names.
    characters = {
        i["name"][0]: {"description": i["description"], "aliases": i["name"][1:]}
        for i in data
        if i["frequency"] > 1
    }

    with open(json_filename, "w") as fp:
        json.dump(
            {"characters": characters, "settings": {}, "quotes": []},
            fp,
            indent=4,
            ensure_ascii=False,
        )


def generateXRayDb(filename: str, db: Database):
    characters = [i for i in db.dump() if i["frequency"] > 1]

    with XRayDb(filename) as xraydb:
        for i in characters:
            xraydb.add_entity(
                Entity(
                    name=i["name"][0],
                    type=EntityType.People,
                    source=EntitySource.Wikipedia,
                    count=i["frequency"],
                    description=i["description"],
                )
            )


async def peakDatabase(filename: str, llm: BaseChatOpenAI, ebd: OpenAIEmbeddings):
    await asyncio.sleep(0)
    db = ChromaDatabase(ebd, filename + ".chroma")
    data = db.dump()
    for i in data:
        print(i["name"], i["frequency"])
        print(i["description"])
        print("=" * 80)

    print("Total items:", len(data))
    dumpDatabese(filename, db)
    generateXRayDb(filename, db)
