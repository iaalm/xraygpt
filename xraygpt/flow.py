import shelve

from loguru import logger

from xraygpt.db.chroma import ChromaDatabase
from xraygpt.llm import get_ebd, get_llm
from xraygpt.ner.agent import recognize_entities
from xraygpt.reader import EPubReader


def epubSummaryFlow(filename):
    people = set()
    for item in EPubReader(filename):
        logger.debug(item)
        people |= recognize_entities([item])
        logger.info(f"# people found so far: {len(people)}")


def epubPeopleFlow(filename):
    state = shelve.open(filename + ".shelve")
    llm = get_llm()
    ebd = get_ebd()
    db = ChromaDatabase(ebd, filename + ".chroma")

    for ix, item in enumerate(EPubReader(filename)):
        if ix <= state.get("last_processed", -1):
            logger.info(f"Skipping {ix}")
            continue
        # logger.debug(item)
        recognize_entities(item, llm, db)

        state["last_processed"] = ix

    for i in db.dump():
        print(i["name"])
        print(i["description"])
        print("=" * 80)


if __name__ == "__main__":
    print(epubPeopleFlow("workdir/InfiniteJest.epub"))
