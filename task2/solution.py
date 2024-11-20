import asyncio

import aiofiles
from aiocsv import AsyncWriter
from aiohttp import ClientSession
from bs4 import BeautifulSoup

BASE = "https://ru.wikipedia.org"


def generate_url(uri: str) -> str:
    return f"{BASE}{uri}"


async def fetch(session: ClientSession, url: str) -> None:
    async with session.get(url) as response:
        return await response.text()


async def parse(html) -> tuple[dict[str, int], str | None]:
    temp = {}

    soup = BeautifulSoup(html, "html.parser")
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


async def to_csv(data: dict, filename: str) -> None:
    async with aiofiles.open(filename, mode="w", encoding="utf-8") as afp:
        writer = AsyncWriter(afp, dialect="unix")
        await writer.writerows(data.items())


async def main() -> None:
    result = {}
    url = "https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту"

    while True:
        async with ClientSession() as session:
            html = await fetch(session, url)
            temp, uri = await parse(html)
            for letter, counts in temp.items():
                result[letter] = result.get(letter, 0) + counts

            if not uri:
                break

            url = generate_url(uri)

    await to_csv(result, "task2/beasts.csv")


if __name__ == "__main__":
    asyncio.run(main())
