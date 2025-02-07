import asyncio
import json

from xraygpt.db.chroma import ChromaDatabase


def dumpDatabese(filename: str, db: ChromaDatabase):
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


async def peakDatabase(filename: str):
    await asyncio.sleep(0)
    db = ChromaDatabase(None, filename + ".chroma")
    data = db.dump()
    for i in data:
        print(i["name"], i["frequency"])
        print(i["description"])
        print("=" * 80)

    print("Total items:", len(data))
    dumpDatabese(filename, db)
