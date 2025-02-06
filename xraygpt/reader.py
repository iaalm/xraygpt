from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


class EPubReader:
    def __init__(self, filename):
        self.book = epub.read_epub(filename, {"ignore_ncx": True})

    def _get_items(self):
        return self.book.get_items_of_type(ITEM_DOCUMENT)

    def __iter__(self):
        self.it = self._get_items()
        return self

    def __next__(self):
        try:
            item = next(self.it)
        except StopIteration:
            raise StopIteration

        soup = BeautifulSoup(item.get_body_content(), "html.parser")
        return soup.get_text()

    def __len__(self):
        return sum(1 for _ in self._get_items())


if __name__ == "__main__":
    for item in EPubReader("workdir/InfiniteJest.epub"):
        print(len(item))
