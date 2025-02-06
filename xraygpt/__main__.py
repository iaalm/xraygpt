import argparse
import asyncio
import logging
import sys

from loguru import logger

from xraygpt.__about__ import __version__
from xraygpt.flow import epubPeopleFlow
from xraygpt.output import peakDatabase

flowname_map = {
    "people": epubPeopleFlow,
    "peak": peakDatabase,
}


def config_log_level(v: int) -> None:
    logger.remove()
    log_format = "<level>{message}</level>"
    if v >= 4:
        logger.add(sys.stderr, level="TRACE", format=log_format)
    elif v >= 3:
        logger.add(sys.stderr, level="DEBUG", format=log_format)
    elif v >= 2:
        logger.add(sys.stderr, level="INFO", format=log_format)
    elif v >= 1:
        logger.add(sys.stderr, level="SUCCESS", format=log_format)
    else:
        logger.add(sys.stderr, level="WARNING", format=log_format)

    if v < 4:
        # avoid "WARNING! deployment_id is not default parameter."
        langchain_logger = logging.getLogger("langchain.chat_models.openai")
        langchain_logger.disabled = True


def main() -> None:
    parser = argparse.ArgumentParser(description="xxy-" + __version__)
    parser.add_argument("-v", action="count", default=0, help="verbose level.")
    parser.add_argument("filename", help="input file name.")
    parser.add_argument(
        "-f", help="flow name", choices=flowname_map.keys(), default="people"
    )

    # create the parser for the "foo" command
    args = parser.parse_args()

    config_log_level(args.v)

    asyncio.run(flowname_map[args.f](args.filename))


if __name__ == "__main__":
    main()
