from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, epub


class EPubReader:
    def __init__(self, filename):
        self.book = epub.read_epub(filename)

    def __iter__(self):
        self.it = self.book.get_items_of_type(ITEM_DOCUMENT)
        return self

    def __next__(self):
        try:
            item = next(self.it)
            soup = BeautifulSoup(item.get_body_content(), "html.parser")
            return soup.get_text()
        except StopIteration:
            raise StopIteration


if __name__ == "__main__":
    for item in EPubReader("workdir/InfiniteJest.epub"):
        print(len(item))
