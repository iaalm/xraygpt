import shelve

from loguru import logger
from tqdm import tqdm

from xraygpt.db.chroma import ChromaDatabase
from xraygpt.llm import get_ebd, get_llm
from xraygpt.ner.agent import recognize_entities
from xraygpt.output import dumpDatabese
from xraygpt.reader import EPubReader


def epubSummaryFlow(filename):
    people = set()
    for item in EPubReader(filename):
        logger.debug(item)
        people |= recognize_entities([item])
        logger.info(f"# people found so far: {len(people)}")


async def epubPeopleFlow(filename):
    state = shelve.open(filename + ".shelve")
    llm = get_llm()
    ebd = get_ebd()
    db = ChromaDatabase(ebd, filename + ".chroma")
    book = EPubReader(filename)

    for ix, item in enumerate(tqdm(book, total=len(book))):
        if ix <= state.get("last_processed", -1):
            logger.debug(f"Skipping {ix}")
            continue
        # logger.debug(item)
        await recognize_entities(item, llm, db)

        state["last_processed"] = ix

    dumpDatabese(filename, db)
