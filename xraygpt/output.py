from xraygpt.db.chroma import ChromaDatabase

def printDatabase():
    db = ChromaDatabase(None, "workdir/db.chroma")
    for i in db.dump():
        print(i["name"])
        print(i["description"])
        print("=" * 80)

if __name__ == "__main__":
    printDatabase()
