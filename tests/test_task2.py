import csv


def test_csv():
    first_letter = ""
    last_letter = ""
    line_count = 0

    with open("task2/beasts.csv", encoding="utf-8") as fp:
        for row in csv.reader(fp):
            if not first_letter:
                first_letter = row[0]

            last_letter = row[0]
            line_count += 1

    assert first_letter == "А"
    assert last_letter == "Z"
    assert line_count == 56
