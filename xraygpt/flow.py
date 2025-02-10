import shelve

from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_openai.chat_models.base import BaseChatOpenAI
from loguru import logger
from tqdm import tqdm

from xraygpt.db.chroma import ChromaDatabase
from xraygpt.db.text_cache import TextCache
from xraygpt.ner.agent import recognize_entities
from xraygpt.output import dumpDatabese
from xraygpt.reader import EPubReader


def epubSummaryFlow(filename):
    people = set()
    for item in EPubReader(filename):
        logger.debug(item)
        people |= recognize_entities([item])
        logger.info(f"# people found so far: {len(people)}")


async def epubPeopleFlow(filename: str, llm: BaseChatOpenAI, ebd: OpenAIEmbeddings):
    state = shelve.open(filename + ".shelve")
    raw_db = ChromaDatabase(ebd, filename + ".chroma")
    db = TextCache(raw_db)
    book = EPubReader(filename)

    bar = tqdm(book, total=len(book))
    for ix, item in enumerate(bar):
        if ix <= state.get("last_processed", -1):
            logger.debug(f"Skipping {ix}")
            continue
        # logger.debug(item)
        logger.trace("Processing {content}", content=item)
        with get_openai_callback() as cb:
            await recognize_entities(item, llm, db)
            logger.trace(f"Total tokens: {cb.total_tokens}")
            state["total_tokens"] = cb.total_tokens + state.get("total_tokens", 0)
        bar.set_postfix(tkn=str(int(state["total_tokens"] / 1000)) + "k")

        state["last_processed"] = ix

    dumpDatabese(filename, db)
