import itertools
from typing import Generator, List


def sillySplit(strs: List[str], max_len) -> Generator[str, None, None]:
    res = ""
    for i in itertools.chain.from_iterable([s.split(".") for s in strs]):
        if len(res) + len(i) + 1 > max_len:
            yield res
            res = ""
        res += i + "."
