import pytest

import aiofiles
from aiocsv import AsyncReader

from task2.solution import parse

html_page_1 = """
    <html>
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>А</h3>
                    <ul><li>Аардоникс</a></li>
                    <ul><li>Абботины</a></li>
                    <ul><li>Абелизавр</a></li>
            </div>
        <a href="/w/index.php?title=test" title="Категория:Животные по алфавиту">Следующая страница</a>
        </div>
    </html>
"""

html_page_2 = """
    <html>
        <div id="mw-pages">
            <div class="mw-category-group">
                <h3>А</h3>
                    <ul>
                        <li>Аардоникс</li>
                        <li>Абботины</li>
                    </ul>
            <div class="mw-category-group">
                <h3>Б</h3>
                    <ul>
                        <li>Бегемот</li>
                    </ul>
            </div>
        <a href="/w/index.php?title=test" title="Категория:Животные по алфавиту">Предыдущая страница</a>
        </div>
    </html>
"""


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (html_page_1, ({"А": 3}, "/w/index.php?title=test")),
        (html_page_2, ({"А": 2, "Б": 1}, None)),
    ],
)
def test_parse(data, expected_result):

    assert parse(data) == expected_result


@pytest.mark.asyncio
async def test_csv():
    first_letter = ""
    last_letter = ""
    line_count = 0

    async with aiofiles.open("task2/beasts.csv", encoding="utf-8") as afp:
        async for row in AsyncReader(afp):
            if not first_letter:
                first_letter = row[0]

            last_letter = row[0]
            line_count += 1

    assert first_letter == "А"
    assert last_letter == "Z"
    assert line_count == 55
