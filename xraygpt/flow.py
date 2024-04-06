from xraygpt.ner import recognize_entities
from xraygpt.reader import EPubReader


def epubSummaryFlow(filename):
    for item in EPubReader(filename):
        print(item)
        recognize_entities([item])
        break


if __name__ == "__main__":
    print(epubSummaryFlow("workdir/InfiniteJest.epub"))
