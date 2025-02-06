from xraygpt.db.chroma import ChromaDatabase


def printDatabase(filename):
    db = ChromaDatabase(None, filename + ".chroma")
    data = db.dump()
    for i in data:
        print(i["name"])
        print(i["description"])
        print("=" * 80)

    print("Total items:", len(data))


if __name__ == "__main__":
    printDatabase("workdir/InfiniteJest.epub")
