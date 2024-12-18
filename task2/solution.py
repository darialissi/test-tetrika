import csv
import logging
from collections import Counter

import wikipediaapi

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def to_csv(data: dict, filename: str) -> None:
    with open(filename, mode="w", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerows(data.items())


def main() -> None:
    wiki = wikipediaapi.Wikipedia("Wiki Parser", "ru")
    page = wiki.page("Категория:Животные_по_алфавиту")

    result = Counter(
        map(
            lambda k: k[0],
            filter(
                lambda k: not k.startswith("Категория:"), page.categorymembers.keys()
            ),
        )
    )

    to_csv(result, "task2/beasts.csv")


if __name__ == "__main__":
    main()
