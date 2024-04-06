import itertools
from typing import List


def sillySplit(strs: List[str], max_len) -> List[str]:
    return [
        i
        for i in itertools.chain.from_iterable([s.split(".") for s in strs])
        if len(i) > 0
    ]
