import asyncio
import logging

import aiofiles
import requests
from aiocsv import AsyncWriter
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def parse(html: str) -> tuple[dict[str, int], str | None]:
    temp = {}

    soup = BeautifulSoup(html, "lxml")
    tag = soup.select_one("#mw-pages")
    groups = tag.select("div.mw-category-group")

    for group in groups:
        letter = group.select_one("h3").text
        titles = group.select_one("ul").select("li")
        counts = sum(map(lambda x: 1, titles))
        temp[letter] = counts

    uri = tag.select_one("a:-soup-contains('Следующая страница')")
    if uri:
        uri = uri.get("href")

    return temp, uri


def get_result() -> dict[str, int]:
    result = {}
    base = "https://ru.wikipedia.org"
    url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"

    while True:
        html = requests.get(url)
        temp, uri = parse(html.text)
        for letter, counts in temp.items():
            result[letter] = result.get(letter, 0) + counts

        if not uri:
            break

        url = f"{base}{uri}"

    return result


async def to_csv(data: dict, filename: str) -> None:
    async with aiofiles.open(filename, mode="w", encoding="utf-8") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        await writer.writerows(data.items())


if __name__ == "__main__":
    logger.info("Started")
    asyncio.run(to_csv(get_result(), "task2/beasts.csv"))
    logger.info("Finished")
